# from email.mime import image
import logging
from gi.repository import Gimp, GLib
from typing import List, Dict, Any

# --- LOCALIZATION SETUP ---
STRINGS = {
    "en": {
        "group_name": "Enhancement Stack",
        "wb_name": "White Balance",
        "det_eq": "Detail Equalization",
        "grey_grp": "Contrast/Grey Mix",
        "orig": "Original"
    },
    "de": {
        "group_name": "Optimierungs-Stapel",
        "wb_name": "Weißabgleich",
        "det_eq": "Detail-Egalisierung",
        "grey_grp": "Kontrast/Grau-Mix",
        "orig": "Original"
    }
}

def get_lang():
    lang = GLib.get_language_names()[0][:2]
    return lang if lang in STRINGS else "en"

L = STRINGS[get_lang()]

logger = logging.getLogger("KonradFilters")

def enhance_image_logic(self, image: Gimp.Image, drawable: Gimp.Drawable):
    image.undo_group_start()
    stats = self._get_cached_stats(drawable)
    size = (((image.get_width()**2) + (image.get_height()**2))**0.5)
    blur_radius = size / 1000.0
    threshold_val = ((stats['mean'] * stats['median'])**0.5) / 255.0
    main_group = Gimp.GroupLayer.new(image)
    main_group.set_name(L['group_name'])
    image.insert_layer(main_group, None, 0)
    drawable.set_name(L['orig'])
    image.insert_layer(drawable, main_group, 0)
    wb_layer = drawable.copy()
    wb_layer.set_name(L['wb_name'])
    image.insert_layer(wb_layer, main_group, 1)
    self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_layer)
    wb_layer.set_opacity(90.0)
    grey_group = Gimp.GroupLayer.new(image)
    grey_group.set_name(L['grey_grp'])
    grey_group.set_mode(Gimp.LayerMode.MULTIPLY)
    grey_group.set_opacity(10.0)
    image.insert_layer(grey_group, main_group, 0)
    wb_grey = wb_layer.copy()
    wb_grey.set_name("grey by white balance")
    image.insert_layer(wb_grey, grey_group, 0)
    self._call_pdb('gimp-drawable-desaturate', drawable=wb_grey)
    self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_grey)
    wb_bw = wb_layer.copy()
    wb_bw.set_name("b/w by white balance (incl blur)")
    image.insert_layer(wb_bw, grey_group, 0)
    filt = Gimp.DrawableFilter.new(wb_bw, "gegl:gaussian-blur", "Blur")
    filt.get_config().set_property("std-dev-x", blur_radius)
    wb_bw.merge_filter(filt)
    self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_bw)
    self._call_pdb('gimp-drawable-threshold', drawable=wb_bw, low_threshold=threshold_val, high_threshold=1.0)
    wb_bw.set_opacity(10.0)
    eq_grey = drawable.copy()
    eq_grey.set_name("grey by equalize")
    image.insert_layer(eq_grey, grey_group, 0)
    self._call_pdb('gimp-drawable-equalize', drawable=eq_grey, mask_only=False)
    self._call_pdb('gimp-drawable-desaturate', drawable=eq_grey)
    eq_grey.set_opacity(50.0)
    eq_bw = drawable.copy()
    eq_bw.set_name("b/w by equalize (incl bright+contrast)")
    image.insert_layer(eq_bw, grey_group, 0)
    self._call_pdb('gimp-drawable-equalize', drawable=eq_bw, mask_only=False)
    self._call_pdb('gimp-drawable-threshold', drawable=eq_bw, low_threshold=threshold_val, high_threshold=1.0)
    eq_bw.set_opacity(10.0)
    det_layer = drawable.copy()
    det_layer.set_name(L['det_eq'])
    image.insert_layer(det_layer, main_group, len(main_group.get_children()))
    mode = Gimp.LayerMode.OVERLAY if stats['mean'] < 128 else Gimp.LayerMode.SCREEN
    det_layer.set_mode(mode)
    det_layer.set_opacity(25.0)
    self._call_pdb('gimp-drawable-equalize', drawable=det_layer, mask_only=False)
    image.undo_group_end()
    Gimp.displays_flush()

class base:
    def __init__(self):
        pass

class image_processor(base):
    def _call_pdb(self, func_name, **kwargs):
        try:
            return Gimp.pdb_call(func_name, **kwargs)
        except Exception as e:
            logger.error(f"Error calling PDB function '{func_name}': {e}")
            raise
        
    def __init__(self):
        super().__init__()

class enhance_image(image_processor):

    def create_wb_grey(
            self, 
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer
        ) -> None:
        wb_grey = drawable.copy()
        wb_grey.set_name("grey by white balance")
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
        """_summary_

        Args:
            image (Gimp.Image): The image to process.
            drawable (Gimp.Drawable): The drawable to process.
            layer_group (Gimp.GroupLayer): The layer group to insert the new layer into.
            blur_radius (float): The radius for the Gaussian blur.
            threshold_val (float): The threshold value for the black and white effect.
        """
        wb_bw = drawable.copy()
        wb_bw.set_name("b/w by white balance (incl blur)")
        image.insert_layer(wb_bw, layer_group, 0)
        # Apply Gaussian blur to the layer
        filt = Gimp.DrawableFilter.new(wb_bw, "gegl:gaussian-blur", "Blur")
        filt.get_config().set_property("std-dev-x", blur_radius)
        wb_bw.merge_filter(filt)
        # Apply white balance adjustment and thresholding to create a black and white effect
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_bw) # white balance adjustment
        self._call_pdb(
            'gimp-drawable-threshold', # apply thresholding to create black and white effect
            drawable=wb_bw,
            low_threshold=threshold_val,
            high_threshold=1.0
        )
        wb_bw.set_opacity(10.0)

    def create_eq_grey(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer
        ) -> None:
        eq_grey = drawable.copy()
        eq_grey.set_name("grey by equalize")
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
        eq_bw = drawable.copy()
        eq_bw.set_name("b/w by equalize (incl bright+contrast)")
        image.insert_layer(eq_bw, layer_group, 0)
        self._call_pdb('gimp-drawable-equalize', drawable=eq_bw, mask_only=False) # apply equalization to enhance contrast
        self._call_pdb(
            'gimp-drawable-threshold', # apply thresholding to create black and white effect
            drawable=eq_bw,
            low_threshold=threshold_val,
            high_threshold=1.0
        )
        eq_bw.set_opacity(10.0)  # Placeholder for the actual implementation

    def create_layer_group(self, image) -> Gimp.GroupLayer:
        layer_group = Gimp.GroupLayer.new(image)
        layer_group.set_name(L['group_name'])
        return layer_group
    
    def create_layer_whitebalace(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer
        ) -> None:
        image.insert_layer(drawable, layer_group, 0)
        wb_layer = drawable.copy()
        wb_layer.set_name(L['wb_name'])
        image.insert_layer(wb_layer, layer_group, 1)
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
        grey_layer_group.set_name(L['grey_grp'])
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
        det_layer.set_name(L['det_eq'])
        image.insert_layer(det_layer, layer_group, len(layer_group.get_children()))
        
        # Apply Gaussian blur to the layer
        filt = Gimp.DrawableFilter.new(det_layer, "gegl:gaussian-blur", "Blur")
        filt.get_config().set_property("std-dev-x", blur_radius)
        det_layer.merge_filter(filt)
        
        mode = Gimp.LayerMode.OVERLAY if image_stats['mean'] < 128 else Gimp.LayerMode.SCREEN
        det_layer.set_mode(mode)
        det_layer.set_opacity(25.0)
        self._call_pdb('gimp-drawable-equalize', drawable=det_layer, mask_only=False)

    def __init__(self, image: Gimp.Image, drawable:Gimp.Drawable) -> None:
        """Initialize the enhancement process.

        Args:
            image (Gimp.Image): The image to be enhanced.
            drawable (Gimp.Drawable): The drawable (layer) to be enhanced.
        """
        super().__init__()
        image.undo_group_start() # Start an undo group for the entire enhancement process
        stats = self._get_cached_stats(drawable) # Get cached statistics for the drawable

        # Calculate prerequisites for enhancement layers
        size = (((image.get_width()**2) + (image.get_height()**2))**0.5)
        blur_radius = size / 1000.0
        threshold_val = ((stats['mean'] * stats['median'])**0.5) / 255.0

        # start layering process
        main_layer_group = self.create_layer_group(image) # Create a group layer for all enhancement layers
        image.insert_layer(main_layer_group, None, 0)
        drawable.set_name(L['orig'])

        self.create_layer_whitebalace(image, drawable, main_layer_group) # Create and insert the white balance layer
        self.create_group_contrast_greymix(image, drawable, main_layer_group, blur_radius, threshold_val) # Create and insert the contrast/grey mix group layer
        self.create_layer_detail_equalization(image, drawable, stats, main_layer_group, blur_radius)
        image.undo_group_end()
        Gimp.displays_flush()

    def _get_cached_stats(self, drawable: Gimp.Drawable) -> Dict[str, Any]:
        # Placeholder for actual implementation to retrieve cached stats
        # In a real scenario, this would compute or retrieve statistics like mean and median
        return {'mean': 128, 'median': 128}