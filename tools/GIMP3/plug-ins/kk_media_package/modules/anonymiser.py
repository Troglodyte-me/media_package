#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from . import ImageProcessor
from gi.repository import Gimp, GLib, Gegl
from typing import List, Dict, Any, Optional

logger = logging.getLogger("Anonymiser")


def black_bar(image, drawable):
    """Create a black bar on a new layer using the current selection.

    The function expects an active non-empty selection. It creates a new
    transparent layer, keeps the current selection as-is, and fills the
    selected area with black on the new layer.
    """
    image.undo_group_start()
    try:
        # Ensure there is an active selection to anonymize.
        has_selection, _, _, _, _ = drawable.mask_intersect()
        if not has_selection:
            Gimp.message("No active selection found. Create a selection first.")
            return

        black_bar_layer = Gimp.Layer.new(
            image,
            "Black Bar",
            image.get_width(),
            image.get_height(),
            drawable.type_with_alpha(),
            100.0,
            Gimp.LayerMode.NORMAL,
        )
        image.insert_layer(black_bar_layer, None, 0)

        # Start from transparency so only selected pixels become visible.
        black_bar_layer.fill(Gimp.FillType.TRANSPARENT)

        Gimp.context_push()
        try:
            Gimp.context_set_foreground(Gegl.Color.new("black"))
            black_bar_layer.edit_fill(Gimp.FillType.FOREGROUND)
        finally:
            Gimp.context_pop()
    finally:
        image.undo_group_end()

    Gimp.displays_flush()

def pixeled(image, drawable):
    # this function will pixelate a selected area in a seperate layer at a selected position, with a selected size and pixelation level. The user will be able to select the position, size and pixelation level (with defaults & smart values).
    # todos:
    ## default values: mid of image, default size: 2% of image height 4x5 dimensions, default opacity: 100%, default orientation: portrait, default pixelation level: 10px
    Gimp.message("Function kk-pixeled is a placeholder.")

def blurred(image, drawable):
    # this function will blur a selected area in a seperate layer at a selected position, with a selected size and blur level. The user will be able to select the position, size and blur level (with defaults & smart values).
    # todos:
    ## default values: mid of image, default size: 2% of image height 4x5 dimensions, default opacity: 100%, default orientation: portrait, default blur level: 10px
    Gimp.message("Function kk-blurred is a placeholder.")


def anonymiser(image, drawable):
    Gimp.message("Function kk-anonymiser is a placeholder.")
