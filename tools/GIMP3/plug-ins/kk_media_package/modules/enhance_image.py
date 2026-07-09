#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from . import ImageProcessor
from gi.repository import Gimp, GLib
from typing import List, Dict, Any, Optional

logger = logging.getLogger("EnhanceImage")


class EnhanceImage(ImageProcessor):
    """Enhance image processing class.
    
    Args:
        image_processor (image_processor): The base image processor class.
    """
    ## Override the threshold calculation to consider both original and new statistics
    def _get_threshold_value(
            self, 
            new_stats: Dict[str, Any],
            orig_stats: Dict[str, Any] = {"mean": 127, "std_dev": 0, "median": 127, "pixels": 0}
        ) -> float:
        """Calculates a threshold value based on image statistics.

        Args:
            orig_stats (Dict[str, Any]): A dictionary containing original image statistics.
            new_stats (Dict[str, Any]): A dictionary containing new image statistics.

        Returns:
            float: The calculated threshold value.
        """
        new_threshold = super()._get_threshold_value(new_stats) * 255.0  # Convert to 0-255 scale
        return ((orig_stats['mean'] + orig_stats['median'] + new_stats['mean'] + new_stats['median'] + new_threshold) / 5) / 255.0
    
    def _get_adaptive_unsharp_settings(
            self,
            blur_radius: float,
            stats: Dict[str, Any] = {"mean": 127, "std_dev": 0, "median": 127, "pixels": 0}
        ) -> Optional[Dict[str, float]]:
        """Return subtle unsharp-mask settings for soft images.

        The decision is based on histogram standard deviation as a simple
        softness proxy. If the image is not soft enough, returns ``None``
        to skip sharpening.

        Args:
            stats (Dict[str, Any]): Cached image statistics.
            blur_radius (float): Size-adaptive blur radius already used in the pipeline.

        Returns:
            Optional[Dict[str, float]]: ``radius``, ``amount`` and ``threshold``
            for the unsharp-mask filter, or ``None`` when sharpening
            should be skipped.
        """
        std_dev = float(stats.get('std_dev', 0.0))
        mid = super()._get_threshold_value(stats) * 255.0 

        # softness in [0, 1]: 0 means already crisp, 1 means very soft/flat
        softness = max(0.0, min(1.0, (55.0 - std_dev) / 30.0))

        # Skip sharpening unless softness is noticeable.
        if softness < 0.20:
            return None

        # Keep this intentionally subtle and below the large local-contrast blur radius.
        radius = max(0.6, min(2.2, blur_radius * (0.22 + 0.28 * softness)))
        amount = max(0.12, min(0.30, 0.12 + 0.18 * softness))

        # Use a small non-zero threshold to avoid boosting noise.
        threshold = 0.06 - (0.03 * softness)
        if mid < 90.0:
            threshold += 0.02
        threshold = max(0.02, min(0.12, threshold))

        return {
            'radius': radius,
            'amount': amount,
            'threshold': threshold
        }

    def _get_auto_threshold_value(
            self,
            new_stats: Dict[str, Any],
            orig_stats: Dict[str, Any] = {"mean": 127, "std_dev": 0, "median": 127, "pixels": 0}
        ) -> float:
        """Estimate an auto threshold similar to GIMP GUI auto behavior.

        This uses histogram summary stats and intentionally biases thresholding
        down for darker images to avoid losing midtone detail.
        """
        n_mean = float(new_stats.get('mean', 127.0))
        n_median = float(new_stats.get('median', 127.0))
        n_std = float(new_stats.get('std_dev', 0.0))

        o_mean = float(orig_stats.get('mean', 127.0))
        o_median = float(orig_stats.get('median', 127.0))

        # Blend current and original luminance center, then normalize to [0, 1].
        center = (0.45 * n_mean) + (0.30 * n_median) + (0.15 * o_mean) + (0.10 * o_median)
        threshold = center / 255.0

        # Dark-scene compensation: lower threshold when overall tone is dark.
        darkness = max(0.0, min(1.0, (128.0 - center) / 128.0))
        threshold -= 0.18 * darkness

        # Low local contrast compensation: nudge down a bit for flatter images.
        flatness = max(0.0, min(1.0, (55.0 - n_std) / 55.0))
        threshold -= 0.06 * flatness

        # Clamp to a practical auto-threshold window.
        return max(0.12, min(0.78, threshold))

    ## Create a new layer group in the given image
    ## maybe move to image_processor class if needed for other purposes
    def create_layer_group(
            self,
            image,
            name: str = "--NEW--",
            parent_layer_group: Optional[Gimp.GroupLayer] = None, 
            level: int = 0) -> Gimp.GroupLayer:
        """Creates a new group layer in the given image."""
        layer_group = Gimp.GroupLayer.new(image)
        desired_name = name if name != "--NEW--" else _("New Layer Group")
        self._set_unique_name(image, layer_group, desired_name)
        image.insert_layer(layer_group, parent_layer_group, level)
        return layer_group
    
    ## --- Enhancement Layer Creation Methods ---
    ## White Balance Layer
    def create_layer_whitebalance(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer
        ) -> None:
        """Creates a white balance layer and inserts it into the given layer group."""
        wb_layer = self._copy_layer(
            image,
            drawable,
            layer_group,
            name=_("White Balance"),
            level=0
        )
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_layer) # white balance adjustment
        wb_layer.set_opacity(90.0)

    ## Contrast/Grey Mix Group Layer
    def create_group_contrast_greymix(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            main_layer_group: Gimp.GroupLayer,
            blur_radius: float,
            stats: Dict[str, Any]
        ) -> None:
        grey_layer_group = self.create_layer_group(
            image,
            name=_("Contrast/Grey Mix"),
            parent_layer_group=main_layer_group,
            level=0,
        )
        grey_layer_group.set_mode(Gimp.LayerMode.MULTIPLY)
        grey_layer_group.set_opacity(10.0)
        
        self.create_wb_grey(image, drawable, grey_layer_group)
        self.create_wb_bw(image, drawable, grey_layer_group, blur_radius, stats)
        self.create_eq_grey(image, drawable, grey_layer_group)
        self.create_eq_bw(image, drawable, grey_layer_group, stats)

    def create_wb_grey(
            self, 
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer
        ) -> None:
        """Creates a grey layer based on white balance."""
        wb_grey = self._copy_layer(
            image,
            drawable,
            layer_group,
            name=_("grey by white balance"),
            level=0
        )
        self._call_pdb('gimp-drawable-desaturate', drawable=wb_grey) # desaturate to grey
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_grey) # white balance adjustment

    def create_wb_bw(
            self, 
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer,
            blur_radius: float,
            stats: Dict[str, Any]
        ) -> None:
        """Creates a black and white layer based on white balance with optional blur.

        Args:
            image (Gimp.Image): The image to process.
            drawable (Gimp.Drawable): The drawable to process.
            layer_group (Gimp.GroupLayer): The layer group to insert the new layer into.
            blur_radius (float): The radius for the Gaussian blur.
            stats (Dict[str, Any]): A dictionary containing image statistics.
        """
        wb_bw = self._copy_layer(
            image,
            drawable,
            layer_group,
            name=_("b/w by white balance (incl blur)"),
            level=0
        )
        self._apply_gaussian_blur(
            drawable=wb_bw,
            std_dev_x=blur_radius / 2,
            std_dev_y=blur_radius / 2,
            label="Blur"
        )
        # Apply white balance adjustment and thresholding to create a black and white effect
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_bw) # white balance adjustment
        temp_stats           = self._get_cached_stats(wb_bw) # Get cached statistics for the drawable
        new_threshold_val = self._get_auto_threshold_value(
            new_stats=temp_stats,
            orig_stats=stats
        )
        self._call_pdb(
            'gimp-drawable-threshold', # apply thresholding to create black and white effect
            drawable=wb_bw,
            low_threshold=new_threshold_val,  # Adjusting threshold based on image statistics
            high_threshold=1.0
        )
        wb_bw.set_opacity(10.0)

    def create_eq_grey(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer
        ) -> None:
        """Creates a grey layer based on equalization."""
        eq_grey = self._copy_layer(
            image,
            drawable,
            layer_group,
            name=_("grey by equalize"),
            level=0
        )
        self._call_pdb('gimp-drawable-equalize', drawable=eq_grey, mask_only=False) # apply equalization to enhance contrast
        self._call_pdb('gimp-drawable-desaturate', drawable=eq_grey) # desaturate to grey
        eq_grey.set_opacity(50.0)

    def create_eq_bw(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer,
            stats: Dict[str, Any]
        ) -> None:
        """Creates a black and white layer based on equalization."""
        eq_bw = self._copy_layer(
            image,
            drawable,
            layer_group,
            name=_("b/w by equalize (incl bright+contrast)"),
            level=0
        )
        self._call_pdb('gimp-drawable-equalize', drawable=eq_bw, mask_only=False) # apply equalization to enhance contrast
        temp_stats           = self._get_cached_stats(eq_bw) # Get cached statistics for the drawable
        new_threshold = self._get_auto_threshold_value(
            new_stats=temp_stats,
            orig_stats=stats
        )
        self._call_pdb(
            'gimp-drawable-threshold', # apply thresholding to create black and white effect
            drawable=eq_bw,
            low_threshold=new_threshold,  # Adjusting threshold based on image statistics
            high_threshold=1.0
        )
        eq_bw.set_opacity(10.0)  # Placeholder for the actual implementation

    ## Pop Enhancement Layer
    ## todo: implement a more sophisticated pop enhancement algorithm, possibly using edge detection or frequency separation techniques.
    def create_layer_pop_enhancement(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            image_stats: Dict[str, Any],
            layer_group: Gimp.GroupLayer,
            blur_radius: float
        ) -> None:
        """Creates a blur-based pop enhancement layer and inserts it into the given layer group."""
        
        # Smart Mode Logic: "Three-Way" Switch
        if   max(image_stats['mean'], image_stats['median']) < 100:
            # Underexposed	Low Mean (< 100)	Screen (Lifts shadows)
            mode = Gimp.LayerMode.SCREEN
        elif min(image_stats['mean'], image_stats['median']) > 160:  # if the image is overexposed, apply a subtle enhancement
            # Overexposed	High Mean (> 160)	Multiply (at very low opacity)
            mode = Gimp.LayerMode.MULTIPLY
        elif image_stats['std_dev'] < 50:  # if the image is flat/dull, apply a moderate enhancement
            # Flat/Dull	Mid Mean, Low StdDev	Overlay (Pushes contrast)
            mode = Gimp.LayerMode.OVERLAY
        elif image_stats['std_dev'] >= 50:  # if the image is balanced, apply a subtle enhancement
            # Balanced	Mid Mean, High StdDev	Soft Light (Subtle "pop")
            mode = Gimp.LayerMode.SOFTLIGHT
        else:
            mode = Gimp.LayerMode.NORMAL  # Default to normal mode if none of the conditions are met

        # Dynamic Variables (Blur and Opacity)
        # blur_radius # done

        # Smart Opacity: Use the "Distance from Neutral" logic.
        threshold = super()._get_threshold_value(stats=image_stats) * 255.0  # Convert to 0-255 scale
        dark = 50
        darker_mid = 100
        lighter_mid = 130
        
        if threshold < dark:  # Very dark image
            opacity = 25.0
        elif threshold < darker_mid:  # Dark image
            opacity = 8.0
            opacity += (darker_mid - threshold) / (darker_mid - dark) * (25.0 - 8.0)  # Scale opacity between 8% and 25%
        elif threshold < lighter_mid:  # quite light image
            opacity = 5.0
            opacity += (lighter_mid - threshold) / (lighter_mid - darker_mid) * (8.0 - 5.0)  # Scale opacity between 5% and 8%
        else:  # Extremely light image
            opacity = 1.0
            opacity += (255.0 - threshold) / (255.0 - lighter_mid) * (5.0 - 1.0)  # Scale opacity between 1% and 5%

        eq_layer = self._copy_layer(
            image,
            drawable,
            layer_group,
            name="Temporary Equalization Layer",
            level=0
        )
        luminosity_layer = self._copy_layer(
            image,
            drawable,
            layer_group,
            name="Temporary Luminosity Layer",
            level=0
        )

        # Apply subtle, adaptive unsharp mask only when the image appears soft.
        unsharp_filt = self._get_adaptive_unsharp_settings(
            blur_radius=blur_radius,
            stats=image_stats
        )
        if unsharp_filt is not None:
            self._apply_unsharp_mask(
                drawable=luminosity_layer,
                radius=unsharp_filt['radius'],
                amount=unsharp_filt['amount'],
                threshold=unsharp_filt['threshold']
            )
        else:
            logger.info("Skipping unsharp mask: image is not soft enough for subtle sharpening.")

        self._call_pdb('gimp-drawable-equalize', drawable=eq_layer, mask_only=False)
        self._apply_gaussian_blur(
            drawable=eq_layer,
            std_dev_x=blur_radius,
            std_dev_y=blur_radius,
            label="Blur"
        )
        
        eq_layer.set_mode(Gimp.LayerMode.NORMAL)

        # Keep luminosity layer on top of equalized layer, then merge into one pop layer
        luminosity_layer.set_mode(Gimp.LayerMode.LUMINANCE)
        luminosity_layer.set_opacity(50.0)
        pop_layer = image.merge_down(luminosity_layer, Gimp.MergeType.EXPAND_AS_NECESSARY)
        self._set_unique_name(image, pop_layer, _("Pop Enhancement (Equalized)"))
        
        pop_layer.set_mode(mode)
        pop_layer.set_opacity(opacity)

    def __init__(self, image: Gimp.Image, drawable:Gimp.Drawable) -> None:
        """Initialize the enhancement process.

        Args:
            image (Gimp.Image): The image to be enhanced.
            drawable (Gimp.Drawable): The drawable (layer) to be enhanced.
        """
        super().__init__()
        image.undo_group_start() # Start an undo group for the entire enhancement process
        # image.insert_layer(drawable, layer_group, 0)
        try:
            # Calculate prerequisites for enhancement layers
            original_name   = drawable.get_name()
            stats           = self._get_cached_stats(drawable) # Get cached statistics for the drawable
            size            = self._get_size(image)
            blur_radius     = self._get_blur_radius(size)
            # threshold_val   = super()._get_threshold_value(stats)
            logger.info(f"Original Name: {original_name}, Image size: {size}, Blur radius: {blur_radius}, Stats: {stats}")

            # start layering process
            main_layer_group = self.create_layer_group( # Create a group layer for all enhancement layers
                image=image, 
                name=f"""{original_name} {_("Enhancement Stack")}""",
                parent_layer_group=None,
                level=0
            )
            self._set_unique_name(image, drawable, _("Original"))

            self.create_layer_whitebalance( # Create and insert the white balance layer
                image=image, 
                drawable=drawable, 
                layer_group=main_layer_group
            ) 
            self.create_group_contrast_greymix( # Create and insert the contrast/grey mix group layer
                image=image,
                drawable=drawable,
                main_layer_group=main_layer_group,
                blur_radius=blur_radius,
                stats=stats
            )
            self.create_layer_pop_enhancement( # Create and insert the blur-based pop enhancement layer
                image=image,
                drawable=drawable,
                image_stats=stats,
                layer_group=main_layer_group,
                blur_radius=blur_radius
            )
        except Exception as e:
            logger.error(f"Error during enhancement process: {e}")
            Gimp.message(f"Error during enhancement process: {e}")
        finally:
            image.undo_group_end()
        Gimp.displays_flush()