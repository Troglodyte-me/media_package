#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import gettext
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio
from typing import List, Dict, Any

# --- FEATURE MODULES ---
from modules.enhance_image import EnhanceImage
from modules.anonymiser import anonymiser, black_bar, pixeled, blurred
from modules.dummy_a import dummy_a_logic

# --- LOGGING ---
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MediaPackageFilters")

# --- LOCALIZATION SETUP ---
# Get the absolute path to this plugin's directory
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALEDIR = os.path.join(PLUGIN_DIR, 'locale')
DOMAIN = "kk_media_package"  # Must match your folder and .mo file names

# Install "_" into Python's built-in namespace globally.
# This makes the _() function automatically available in any imported module (like enhance_image.py)
gettext.install(DOMAIN, LOCALEDIR)

class MediaPackageFiltersPlugin(Gimp.PlugIn):
    # --- STATISTICS ENGINE (OPTIMIZATION) ---
    def _get_cached_stats(self, drawable: Gimp.Drawable) -> Dict[str, Any]:
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
    def _call_pdb(self, proc_name: str, **kwargs) -> Any:
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
    def do_query_procedures(self) -> List[str]:
        return ["kk-enhance-image", "kk-anonymiser", "kk-dummy-a", "kk-black-bar", "kk-pixeled", "kk-blurred"]

    def do_create_procedure(self, name: str) -> Gimp.ImageProcedure:
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None
        )
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.DRAWABLE)
        # --- MENU AND DOCUMENTATION SETUP ---
        # Image Enhancement
        if name == "kk-enhance-image":
            procedure.set_menu_label(_("Enhance Image"))
            procedure.add_menu_path("<Image>/" + _("Filters/Enhance"))
            procedure.set_documentation(
                _("procedure description for Enhance Image"),
                _("Python descripon for Enhance Image"),
                name
            )

        ## Anonymiser and related functions
        elif name == "kk-anonymiser":
            procedure.set_menu_label(_("Anonymiser Wizzard"))
            procedure.add_menu_path("<Image>/" + _("Filters/Enhance/Anonymiser"))
            procedure.set_documentation(
                _("procedure description for Anonymiser"),
                _("Python description for Anonymiser"),
                name
            )
        elif name == "kk-black-bar":
            procedure.set_menu_label(_("Black Bar"))
            procedure.add_menu_path("<Image>/" + _("Filters/Enhance/Anonymiser"))
        elif name == "kk-pixeled":
            procedure.set_menu_label(_("Pixeled"))
            procedure.add_menu_path("<Image>/" + _("Filters/Enhance/Anonymiser"))
        elif name == "kk-blurred":
            procedure.set_menu_label(_("Blurred"))
            procedure.add_menu_path("<Image>/" + _("Filters/Enhance/Anonymiser"))

        ## placeholder for future dummy functions
        elif name == "kk-dummy-a":
            procedure.set_menu_label(_("Dummy A"))
            procedure.add_menu_path("<Image>/" + _("Filters/Dummy"))
        procedure.set_attribution("Konrad Keck (nigma1985)", "2024-2026", "2024")
        return procedure

    def run(
            self,
            procedure: Gimp.ImageProcedure,
            run_mode,
            image: Gimp.Image,
            drawables: List[Gimp.Drawable],
            config: GLib.Variant,
            run_data: GLib.Variant
        ):
        if not drawables:
            return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())
        name = procedure.get_name()
        if name == "kk-enhance-image":
            EnhanceImage(image, drawables[0])
        elif name == "kk-anonymiser":
            anonymiser(image, drawables[0])
        elif name == "kk-black-bar":
            black_bar(image, drawables[0])
        elif name == "kk-pixeled":
            pixeled(image, drawables[0])
        elif name == "kk-blurred":
            blurred(image, drawables[0])
        elif name == "kk-dummy-a":
            dummy_a_logic(image, drawables[0])
        else:
            Gimp.message(f"Function {name} is a placeholder.")
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

if __name__ == "__main__":
    Gimp.main(MediaPackageFiltersPlugin.__gtype__, sys.argv)