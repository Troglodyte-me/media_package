#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from . import ImageProcessor
from gi.repository import Gimp, GLib, Gegl
from typing import List, Dict, Any, Optional

logger = logging.getLogger("Anonymiser")

def check_selection(drawable: Gimp.Drawable) -> bool:
    """Check if there is an active selection in the drawable."""
    has_selection, _, _, _, _ = drawable.mask_intersect()
    return has_selection

def convert_selection_to_dimensions(
        selection: Gimp.Selection,
        pos_x: int, pos_y: int,
        width_by_height: str = "1:1"
    ) -> Optional[Gimp.Selection]:
    """Convert the current selection to a black bar shape.

    This function assumes that there is an active selection. It calculates
    the bounding box of the selection and returns a new selection that
    represents a black bar covering the selected area.
    """
    try:
        # Get the bounding box of the current selection
        bbox = selection.get_bounds()
        if bbox is None:
            logger.warning("No active selection found.")
            return None

        # Calculate the new dimensions for the black bar
        new_x = bbox.x + pos_x
        new_y = bbox.y + pos_y
        width_ratio, height_ratio = map(int, width_by_height.split(":"))
        new_width = bbox.width * width_ratio // (width_ratio + height_ratio)
        new_height = bbox.height * height_ratio // (width_ratio + height_ratio)

        # Create a new selection representing the black bar
        new_selection = Gimp.Selection.new_rectangle(new_x, new_y, new_width, new_height)
        return new_selection
    except Exception as e:
        logger.error(f"Error converting selection to dimensions: {e}")
        return None
    # Placeholder for actual implementation
    # In a real implementation, you would calculate the bounding box of the selection
    # and create a new selection that represents a black bar.
    # return None  # Replace with actual selection conversion logic

#################################################

def black_bar(image, drawable):
    """Create a black bar on a new layer using the current selection.

    The function expects an active non-empty selection. It creates a new
    transparent layer, keeps the current selection as-is, and fills the
    selected area with black on the new layer.
    """
    image.undo_group_start()
    try:
        # Ensure there is an active selection to anonymize.
        if not check_selection(drawable):
            Gimp.message(_("No active selection found. Please select an area to anonymize."))
            return

        original_selection = drawable.get_selection()
        new_selection = convert_selection_to_dimensions(original_selection, pos_x=x, pos_y=y, width_by_height="4:1")
        drawable.set_selection(new_selection)
        
        black_bar_layer = Gimp.Layer.new(
            image,
            _("Black Bar"),
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
        drawable.set_selection(original_selection)
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
