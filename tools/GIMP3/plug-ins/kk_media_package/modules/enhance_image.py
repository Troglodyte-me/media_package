import logging
# import os
# import gettext
# from email.mime import image
from gi.repository import Gimp, GLib
from typing import List, Dict, Any

logger = logging.getLogger("KonradFilters")

class base:
    def __init__(self):
        pass

class image_processor(base):
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
        
    def __init__(self):
        super().__init__()

class enhance_image(image_processor):
    """Enhance image processing class.
    
    Args:
        image_processor (image_processor): The base image processor class.
    """
    def create_wb_grey(
            self, 
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer
        ) -> None:
        """Creates a grey layer based on white balance."""
        wb_grey = drawable.copy()
        wb_grey.set_name(_("grey by white balance"))
        image.insert_layer(wb_grey, layer_group, 0)
        self._call_pdb('gimp-drawable-desaturate', drawable=wb_grey) # desaturate to grey
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_grey) # white balance adjustment

    def create_wb_bw(
            self, 
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer,
            blur_radius: float,
            threshold_val: float
        ) -> None:
        """Creates a black and white layer based on white balance with optional blur.

        Args:
            image (Gimp.Image): The image to process.
            drawable (Gimp.Drawable): The drawable to process.
            layer_group (Gimp.GroupLayer): The layer group to insert the new layer into.
            blur_radius (float): The radius for the Gaussian blur.
            threshold_val (float): The threshold value for the black and white effect.
        """
        wb_bw = drawable.copy()
        wb_bw.set_name(_("b/w by white balance (incl blur)"))
        image.insert_layer(wb_bw, layer_group, 0)
        # Apply Gaussian blur to the layer
        filt = Gimp.DrawableFilter.new(wb_bw, "gegl:gaussian-blur", "Blur")
        filt.get_config().set_property("std-dev-x", blur_radius/2)  # Adjusting blur radius for better effect
        filt.get_config().set_property("std-dev-y", blur_radius/2)  # Adjusting blur radius for better effect
        wb_bw.merge_filter(filt)
        # Apply white balance adjustment and thresholding to create a black and white effect
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_bw) # white balance adjustment
        temp_stats           = self._get_cached_stats(wb_bw) # Get cached statistics for the drawable
        temp_threshold_val   = self.get_threshold_value(temp_stats)
        new_threshold_val = (threshold_val + temp_threshold_val + (temp_stats['median']/255)) / 3
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
        eq_grey = drawable.copy()
        eq_grey.set_name(_("grey by equalize"))
        image.insert_layer(eq_grey, layer_group, 0)
        self._call_pdb('gimp-drawable-equalize', drawable=eq_grey, mask_only=False) # apply equalization to enhance contrast
        self._call_pdb('gimp-drawable-desaturate', drawable=eq_grey) # desaturate to grey
        eq_grey.set_opacity(50.0)

    def create_eq_bw(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer,
            threshold_val: float
        ) -> None:
        """Creates a black and white layer based on equalization."""
        eq_bw = drawable.copy()
        eq_bw.set_name(_("b/w by equalize (incl bright+contrast)"))
        image.insert_layer(eq_bw, layer_group, 0)
        self._call_pdb('gimp-drawable-equalize', drawable=eq_bw, mask_only=False) # apply equalization to enhance contrast
        temp_stats           = self._get_cached_stats(eq_bw) # Get cached statistics for the drawable
        temp_threshold_val   = self.get_threshold_value(temp_stats)
        new_threshold = (threshold_val + temp_threshold_val + (temp_stats['median'] / 255)) / 3
        self._call_pdb(
            'gimp-drawable-threshold', # apply thresholding to create black and white effect
            drawable=eq_bw,
            low_threshold=new_threshold,  # Adjusting threshold based on image statistics
            high_threshold=1.0
        )
        eq_bw.set_opacity(10.0)  # Placeholder for the actual implementation

    def create_layer_group(self, image, name: str = "--NEW--") -> Gimp.GroupLayer:
        """Creates a new group layer in the given image."""
        layer_group = Gimp.GroupLayer.new(image)
        layer_group.set_name(name if name != "--NEW--" else _("New Layer Group"))
        return layer_group
    
    def create_layer_whitebalace(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer
        ) -> None:
        """Creates a white balance layer and inserts it into the given layer group."""
        wb_layer = drawable.copy()
        wb_layer.set_name(_("White Balance"))
        image.insert_layer(wb_layer, layer_group, 0)
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_layer) # white balance adjustment
        wb_layer.set_opacity(90.0)
        
    def create_group_contrast_greymix(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            main_layer_group: Gimp.GroupLayer,
            blur_radius: float,
            threshold_val: float
        ) -> None:
        grey_layer_group = self.create_layer_group(image)
        grey_layer_group.set_name(_("Contrast/Grey Mix"))
        grey_layer_group.set_mode(Gimp.LayerMode.MULTIPLY)
        grey_layer_group.set_opacity(10.0)
        image.insert_layer(grey_layer_group, main_layer_group, 0)
        
        self.create_wb_grey(image, drawable, grey_layer_group)
        self.create_wb_bw(image, drawable, grey_layer_group, blur_radius, threshold_val)
        self.create_eq_grey(image, drawable, grey_layer_group)
        self.create_eq_bw(image, drawable, grey_layer_group, threshold_val)
        
    def create_layer_detail_equalization(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            image_stats: Dict[str, Any],
            layer_group: Gimp.GroupLayer,
            blur_radius: float
        ) -> None:
        det_layer = drawable.copy()
        det_layer.set_name(_("Detail Equalize"))
        image.insert_layer(det_layer, layer_group, 0)
        
        # Apply Gaussian blur to the layer
        filt = Gimp.DrawableFilter.new(det_layer, "gegl:gaussian-blur", "Blur")
        filt.get_config().set_property("std-dev-x", blur_radius)
        filt.get_config().set_property("std-dev-y", blur_radius)
        det_layer.merge_filter(filt)
        
        mode = Gimp.LayerMode.OVERLAY if image_stats['mean'] < 128 else Gimp.LayerMode.SCREEN
        det_layer.set_mode(mode)
        det_layer.set_opacity(25.0)
        self._call_pdb('gimp-drawable-equalize', drawable=det_layer, mask_only=False)

    def get_size(self, image: Gimp.Image) -> float:
        """Calculates the size of the image based on its dimensions.

        Args:
            image (Gimp.Image): The image to calculate the size for.

        Returns:
            float: The calculated size.
        """
        return (((image.get_width()**2) + (image.get_height()**2))**0.5)

    def get_blur_radius(self, size: float) -> float:
        """Calculates a blur radius based on the image size.

        Args:
            size (float): The size of the image.

        Returns:
            float: The calculated blur radius.
        """
        return size / 1000.0

    def get_threshold_value(self, stats: Dict[str, Any]) -> float:
        """Calculates a threshold value based on image statistics.

        Args:
            stats (Dict[str, Any]): A dictionary containing image statistics.

        Returns:
            float: The calculated threshold value.
        """
        return ((stats['mean'] * stats['median'])**0.5) / 255.0

    def __init__(self, image: Gimp.Image, drawable:Gimp.Drawable) -> None:
        """Initialize the enhancement process.

        Args:
            image (Gimp.Image): The image to be enhanced.
            drawable (Gimp.Drawable): The drawable (layer) to be enhanced.
        """
        super().__init__()
        image.undo_group_start() # Start an undo group for the entire enhancement process
        # image.insert_layer(drawable, layer_group, 0)

        # Calculate prerequisites for enhancement layers
        original_name   = drawable.get_name()
        stats           = self._get_cached_stats(drawable) # Get cached statistics for the drawable
        size            = self.get_size(image)
        blur_radius     = self.get_blur_radius(size)
        threshold_val   = self.get_threshold_value(stats)
        logger.info(f"Original Name: {original_name}, Image size: {size}, Blur radius: {blur_radius}, Threshold value: {threshold_val}")

        # start layering process
        main_layer_group = self.create_layer_group( # Create a group layer for all enhancement layers
            image=image, 
            name=f"""{original_name} {_("Enhancement Stack")}"""
        )
        image.insert_layer(main_layer_group, None, 0)
        drawable.set_name(_("Original"))

        self.create_layer_whitebalace(# Create and insert the white balance layer
            image=image, 
            drawable=drawable, 
            layer_group=main_layer_group
        ) 
        self.create_group_contrast_greymix( # Create and insert the contrast/grey mix group layer
            image=image,
            drawable=drawable,
            main_layer_group=main_layer_group,
            blur_radius=blur_radius,
            threshold_val=threshold_val)
        self.create_layer_detail_equalization( # Create and insert the detail equalization layer
            image=image,
            drawable=drawable,
            image_stats=stats,
            layer_group=main_layer_group,
            blur_radius=blur_radius
        )
        image.undo_group_end()
        Gimp.displays_flush()

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