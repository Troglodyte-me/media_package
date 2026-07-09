#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from gi.repository import Gimp, GLib
from typing import List, Dict, Any, Optional

logger = logging.getLogger("KonradFilters")

class Base:
    def __init__(self):
        pass

class ImageProcessor(Base):
    def _set_unique_name(self, image: Gimp.Image, item: Any, desired_name: str) -> str:
        """Set a unique name for an image item by appending numbered suffixes.

        If ``desired_name`` already exists in the image, this method uses
        ``"<name> (2)"``, ``"<name> (3)"``, ... until a free name is found.

        Args:
            image (Gimp.Image): The image containing the item.
            item (Any): The item to be renamed (layer/group/drawable).
            desired_name (str): Preferred name.

        Returns:
            str: The effective unique name that was assigned.
        """
        existing_names = set()

        def _collect_names(layer_items: Any) -> None:
            for layer in layer_items or []:
                try:
                    if layer != item:
                        existing_names.add(layer.get_name())
                except Exception:
                    continue
                try:
                    children = layer.get_children()
                except Exception:
                    children = None
                if children:
                    _collect_names(children)

        try:
            _collect_names(image.get_layers())
        except Exception:
            # Best effort: if layers cannot be listed, keep requested name.
            pass

        effective_name = desired_name
        if effective_name in existing_names:
            idx = 2
            while f"{desired_name} ({idx})" in existing_names:
                idx += 1
            effective_name = f"{desired_name} ({idx})"

        item.set_name(effective_name)
        return effective_name

    def _call_pdb(self, proc_name: str, **kwargs) -> Any:
        """Calls a PDB procedure with the given arguments.

        Args:
            proc_name (str): The name of the PDB procedure to call.

        Raises:
            RuntimeError: If the PDB procedure is not found.
            RuntimeError: If the PDB procedure fails to run.


        Returns:
            Any: The result of the PDB procedure.
        """
        pdb = Gimp.get_pdb()
        proc = pdb.lookup_procedure(proc_name)
        if not proc:
            logger.error(f"PDB procedure '{proc_name}' not found.")
            raise RuntimeError(f"PDB procedure '{proc_name}' not found.")
        config = proc.create_config()
        for k, v in kwargs.items():
            try:
                config.set_property(k, v)
            except Exception as e:
                logger.error(f"Failed to set property '{k}' for '{proc_name}': {e}")
                raise
        logger.info(f"Calling PDB: {proc_name} with args: {kwargs}")
        try:
            result = proc.run(config)
        except Exception as e:
            logger.error(f"Error running PDB procedure '{proc_name}': {e}")
            raise
        if result.index(0) != Gimp.PDBStatusType.SUCCESS:
            logger.error(f"PDB procedure '{proc_name}' failed with status: {result.index(0)}")
            raise RuntimeError(f"PDB procedure '{proc_name}' failed with status: {result.index(0)}")
        return result

    def _copy_layer(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer,
            name: Optional[str] = None,
            level: Optional[int] = 0
        ) -> Gimp.Layer:
        """Creates a copy of the given drawable and inserts it into the specified layer group.

        Args:
            image (Gimp.Image): The image to which the layer belongs.
            drawable (Gimp.Drawable): The drawable to copy.
            layer_group (Gimp.GroupLayer): The group layer to insert the new layer into.
            name (Optional[str]): The name for the new layer.

        Returns:
            Gimp.Layer: The newly created layer.
        """
        new_layer = drawable.copy()
        desired_name = name if name else _("Copy of ") + drawable.get_name()
        self._set_unique_name(image, new_layer, desired_name)
        image.insert_layer(new_layer, layer_group, level)
        return new_layer

    # --- STATISTICS ENGINE (OPTIMIZATION) ---
    def _get_cached_stats(self, drawable: Gimp.Drawable) -> Dict[str, Any]:
        """Calculate and return histogram-based statistics for a drawable.

        This helper queries GIMP's ``gimp-drawable-histogram`` procedure once
        and returns values used by enhancement steps.

        Args:
            drawable: The source drawable to analyze.

        Returns:
            A dictionary containing:
                - ``mean`` (float): Mean value of the VALUE histogram channel.
                - ``std_dev`` (float): Standard deviation of pixel values.
                - ``median`` (float): Median value of pixel values.
                - ``pixels`` (int): Number of pixels considered.

            If histogram retrieval fails, returns fallback defaults:
            ``{"mean": 127, "std_dev": 0, "median": 127, "pixels": 0}``.
        """
        hist_proc = Gimp.get_pdb().lookup_procedure('gimp-drawable-histogram')
        hist_config = hist_proc.create_config()
        hist_config.set_property('drawable', drawable)
        hist_config.set_property('channel', Gimp.HistogramChannel.VALUE)
        hist_config.set_property('start-range', 0.0)
        hist_config.set_property('end-range', 1.0)
        res = hist_proc.run(hist_config)

        if res.index(0) == Gimp.PDBStatusType.SUCCESS:
            return {
                "mean": res.index(1),
                "std_dev": res.index(2),
                "median": res.index(3),
                "pixels": res.index(4)
            }
        return {"mean": 127, "std_dev": 0, "median": 127, "pixels": 0}
    
    def _get_size(self, image: Gimp.Image) -> float:
        """Calculates the size of the image based on its dimensions.

        Args:
            image (Gimp.Image): The image to calculate the size for.

        Returns:
            float: The calculated size.
        """
        return (((image.get_width()**2) + (image.get_height()**2))**0.5)

    def _get_blur_radius(self, size: float) -> float:
        """Calculates a blur radius based on the image size.

        Args:
            size (float): The size of the image.

        Returns:
            float: The calculated blur radius.
        """
        return size / 1000.0

    def _apply_unsharp_mask(
            self,
            drawable: Gimp.Drawable,
            radius: float,
            amount: float,
            threshold: float
        ) -> None:
        """Apply unsharp masking through the GEGL filter backend.

        The legacy PDB procedure ``gimp-drawable-unsharp-mask`` is not
        available in this GIMP3 setup, so we apply ``gegl:unsharp-mask``
        directly on the drawable.
        """
        filt = Gimp.DrawableFilter.new(drawable, "gegl:unsharp-mask", "Unsharp Mask")
        cfg = filt.get_config()
        cfg.set_property("std-dev", radius)
        cfg.set_property("scale", amount)
        cfg.set_property("threshold", threshold)
        drawable.merge_filter(filt)

    def _get_threshold_value(self, stats: Dict[str, Any]) -> float:
        """Calculates a threshold value based on image statistics.

        Args:
            stats (Dict[str, Any]): A dictionary containing image statistics.

        Returns:
            float: The calculated threshold value.
        """
        return ((stats['mean'] * stats['median'])**0.5) / 255.0
    
    def __init__(self):
        super().__init__()

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
        # Apply Gaussian blur to the layer
        filt = Gimp.DrawableFilter.new(wb_bw, "gegl:gaussian-blur", "Blur")
        filt.get_config().set_property("std-dev-x", blur_radius/2)  # Adjusting blur radius for better effect
        filt.get_config().set_property("std-dev-y", blur_radius/2)  # Adjusting blur radius for better effect
        wb_bw.merge_filter(filt)
        # Apply white balance adjustment and thresholding to create a black and white effect
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_bw) # white balance adjustment
        temp_stats           = self._get_cached_stats(wb_bw) # Get cached statistics for the drawable
        new_threshold_val = self._get_threshold_value(
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
        new_threshold = self._get_threshold_value(
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

        # Apply Gaussian blur to the layer
        blr_filt = Gimp.DrawableFilter.new(eq_layer, "gegl:gaussian-blur", "Blur")
        blr_filt.get_config().set_property("std-dev-x", blur_radius)
        blr_filt.get_config().set_property("std-dev-y", blur_radius)
        
        self._call_pdb('gimp-drawable-equalize', drawable=eq_layer, mask_only=False)
        eq_layer.merge_filter(blr_filt)
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