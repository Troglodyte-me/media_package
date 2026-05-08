import logging
from gi.repository import Gimp, GLib

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

def enhance_image_logic(self, image, drawable):
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
