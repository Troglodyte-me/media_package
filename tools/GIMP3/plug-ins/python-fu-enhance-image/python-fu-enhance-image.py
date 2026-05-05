#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio
import logging

# --- LOCALIZATION SETUP ---
# To add languages, add keys to this dictionary
STRINGS = {
    "en": {
        "menu_path": "<Image>/Filters/Konrad's Filters/",
        "enhance_label": "Create Image Enhancement Layers",
        "dummy_a": "Dummy Filter A",
        "dummy_b": "Dummy Filter B",
        "group_name": "Enhancement Stack",
        "wb_name": "White Balance",
        "det_eq": "Detail Equalization",
        "grey_grp": "Contrast/Grey Mix",
        "orig": "Original"
    },
    "de": {
        "menu_path": "<Image>/Filters/Konrads Filter/",
        "enhance_label": "Bildoptimierungs-Ebenen erstellen",
        "dummy_a": "Platzhalter Filter A",
        "dummy_b": "Platzhalter Filter B",
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

# --- LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KonradFilters")

class KonradFiltersPlugin(Gimp.PlugIn):
    
    # --- STATISTICS ENGINE (OPTIMIZATION) ---
    def _get_cached_stats(self, drawable):
        """Calculates stats once to prevent sluggish performance."""
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

    # --- PDB WRAPPERS ---
    def _call_pdb(self, proc_name, **kwargs):
        """
        Calls a GIMP PDB procedure by name with keyword arguments as properties.
        Logs the call and handles errors gracefully.
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

    # --- CORE LOGIC ---
    def enhance_image_logic(self, image, drawable):
        image.undo_group_start()

        # 1. Cache Stats (SPEED GAIN)
        stats = self._get_cached_stats(drawable)
        size = (((image.get_width()**2) + (image.get_height()**2))**0.5)
        blur_radius = size / 1000.0
        threshold_val = ((stats['mean'] * stats['median'])**0.5) / 255.0


        # 2. Create Main Group
        main_group = Gimp.GroupLayer.new(image)
        main_group.set_name(L['group_name'])
        image.insert_layer(main_group, None, 0)

        # 3. Insert Original at bottom of main group
        drawable.set_name(L['orig'])
        image.insert_layer(drawable, main_group, 0)

        # 4. Create White Balance Layer (Copy of Original)
        wb_layer = drawable.copy()
        wb_layer.set_name(L['wb_name'])
        image.insert_layer(wb_layer, main_group, 1)
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_layer)
        wb_layer.set_opacity(90.0)

        # 4. Create Contrast/Grey Group (GIMP2 logic)
        grey_group = Gimp.GroupLayer.new(image)
        grey_group.set_name(L['grey_grp'])
        grey_group.set_mode(Gimp.LayerMode.MULTIPLY)
        grey_group.set_opacity(10.0)
        image.insert_layer(grey_group, main_group, 0)

        # --- grey by white balance ---
        wb_grey = wb_layer.copy()
        wb_grey.set_name("grey by white balance")
        image.insert_layer(wb_grey, grey_group, 0)
        self._call_pdb('gimp-drawable-desaturate', drawable=wb_grey)
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_grey)

        # --- b/w by white balance (incl blur) ---
        wb_bw = wb_layer.copy()
        wb_bw.set_name("b/w by white balance (incl blur)")
        image.insert_layer(wb_bw, grey_group, 0)
        filt = Gimp.DrawableFilter.new(wb_bw, "gegl:gaussian-blur", "Blur")
        filt.get_config().set_property("std-dev-x", blur_radius)
        filt.get_config().set_property("std-dev-y", blur_radius)
        wb_bw.merge_filter(filt)
        self._call_pdb('gimp-drawable-levels-stretch', drawable=wb_bw)
        self._call_pdb('gimp-drawable-threshold', drawable=wb_bw, low_threshold=threshold_val, high_threshold=1.0)
        wb_bw.set_opacity(10.0)

        # --- grey by equalize ---
        eq_grey = drawable.copy()
        eq_grey.set_name("grey by equalize")
        image.insert_layer(eq_grey, grey_group, 0)
        self._call_pdb('gimp-drawable-equalize', drawable=eq_grey, mask_only=False)
        self._call_pdb('gimp-drawable-desaturate', drawable=eq_grey)
        eq_grey.set_opacity(50.0)

        # --- b/w by equalize (incl bright+contrast) ---
        eq_bw = drawable.copy()
        eq_bw.set_name("b/w by equalize (incl bright+contrast)")
        image.insert_layer(eq_bw, grey_group, 0)
        self._call_pdb('gimp-drawable-equalize', drawable=eq_bw, mask_only=False)
        # Brightness/contrast: GIMP 3 PDB may not have direct call, skip or implement if needed
        self._call_pdb('gimp-drawable-threshold', drawable=eq_bw, low_threshold=threshold_val, high_threshold=1.0)
        eq_bw.set_opacity(10.0)

        # 5. Detail Equalization (insert at top of main group)
        det_layer = drawable.copy()
        det_layer.set_name(L['det_eq'])
        # Insert at the top (highest index)
        image.insert_layer(det_layer, main_group, len(main_group.get_children()))
        mode = Gimp.LayerMode.OVERLAY if stats['mean'] < 128 else Gimp.LayerMode.SCREEN
        det_layer.set_mode(mode)
        det_layer.set_opacity(25.0)
        self._call_pdb('gimp-drawable-equalize', drawable=det_layer, mask_only=False)

        image.undo_group_end()
        Gimp.displays_flush()

    # --- GIMP 3 PLUGIN ARCHITECTURE ---
    def do_query_procedures(self):
        return ["python-fu-enhance-image", "python-fu-dummy-a", "python-fu-dummy-b"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run, None)
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE)
        
        if name == "python-fu-enhance-image":
            procedure.set_menu_label(L['enhance_label'])
            procedure.add_menu_path(L['menu_path'])
            procedure.set_documentation("Enhance layers using GIMP 2 legacy logic ported to GIMP 3", "", name)
        elif name == "python-fu-dummy-a":
            procedure.set_menu_label(L['dummy_a'])
            procedure.add_menu_path(L['menu_path'])
        elif name == "python-fu-dummy-b":
            procedure.set_menu_label(L['dummy_b'])
            procedure.add_menu_path(L['menu_path'])
        
        procedure.set_attribution("Konrad Keck", "2024", "2024")
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if not drawables:
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())
        
        name = procedure.get_name()
        if name == "python-fu-enhance-image":
            self.enhance_image_logic(image, drawables[0])
        else:
            # Placeholder for Dummy functions
            Gimp.message(f"Function {name} is a placeholder.")
            
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

if __name__ == "__main__":
    Gimp.main(KonradFiltersPlugin.__gtype__, sys.argv)
