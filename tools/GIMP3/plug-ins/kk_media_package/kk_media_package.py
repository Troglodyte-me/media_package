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

# --- FEATURE MODULES ---
from features.enhance_image import enhance_image_logic
from features.dummy_a import dummy_a_logic
from features.dummy_b import dummy_b_logic

# --- LOCALIZATION SETUP ---
# To add languages, add keys to this dictionary
STRINGS = {
    "en": {
        "menu_path": "<Image>/Filters/Media Package/",
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
        "menu_path": "<Image>/Filters/Medien Paket/",
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

    # --- GIMP 3 PLUGIN ARCHITECTURE ---
    def do_query_procedures(self):
        return ["kk-enhance-image", "kk-dummy-a", "kk-dummy-b"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name, Gimp.PDBProcType.PLUGIN, self.run, None)
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE)
        if name == "kk-enhance-image":
            procedure.set_menu_label(L['enhance_label'])
            procedure.add_menu_path(L['menu_path'])
            procedure.set_documentation(
                "Creates a stack of enhancement layers for the active image using ported GIMP 2 logic. "
                "Parameters: image (Gimp.Image), drawable (Gimp.Drawable). "
                "Output: Enhancement layers grouped for further editing.",
                "This procedure enhances the image by adding multiple adjustment layers such as white balance, detail equalization, and contrast/grey mix. "
                "It is intended for use on RGB images and returns the enhanced image with new layers grouped under a common group.",
                name
            )
        elif name == "kk-dummy-a":
            procedure.set_menu_label(L['dummy_a'])
            procedure.add_menu_path(L['menu_path'])
        elif name == "kk-dummy-b":
            procedure.set_menu_label(L['dummy_b'])
            procedure.add_menu_path(L['menu_path'])
        procedure.set_attribution("Konrad Keck", "2024", "2024")
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if not drawables:
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())
        name = procedure.get_name()
        if name == "kk-enhance-image":
            enhance_image_logic(self, image, drawables[0])
        elif name == "kk-dummy-a":
            dummy_a_logic(self, image, drawables[0])
        elif name == "kk-dummy-b":
            dummy_b_logic(self, image, drawables[0])
        else:
            Gimp.message(f"Function {name} is a placeholder.")
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

if __name__ == "__main__":
    Gimp.main(KonradFiltersPlugin.__gtype__, sys.argv)
