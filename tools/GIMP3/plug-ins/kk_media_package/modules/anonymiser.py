#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from . import ImageProcessor
from gi.repository import Gimp, GLib, Gegl
from typing import List, Dict, Any, Optional

logger = logging.getLogger("Anonymiser")

# Helper translation function if not defined globally
try:
    _
except NameError:
    _ = lambda x: x

def check_selection(drawable: Gimp.Drawable) -> bool:
    """Check if there is an active selection in the drawable."""
    has_selection, _, _, _, _ = drawable.mask_intersect()
    return has_selection

def convert_selection_to_dimensions(
        image: Gimp.Image,
        width_by_height: str = "1:1"
    ) -> Optional[tuple]:
    """Calculate the dimensions for a black bar based on the current selection.

    This function calculates the bounding box of the active selection and returns
    (new_x, new_y, new_width, new_height) representing the centered black bar.
    """
    try:
        selection = image.get_selection()
        if selection is None:
            logger.warning("No active selection found.")
            return None

        # GIMP 3 selection.bounds returns: (success, non_empty, x1, y1, x2, y2)
        success, non_empty, x1, y1, x2, y2 = selection.bounds(image)
        if not success or not non_empty:
            logger.warning("No active selection bounds found.")
            return None

        width = x2 - x1
        height = y2 - y1

        # Calculate the new dimensions for the black bar
        width_ratio, height_ratio = map(int, width_by_height.split(":"))
        new_width = width * width_ratio // (width_ratio + height_ratio)
        new_height = height * height_ratio // (width_ratio + height_ratio)
        
        # Keep the new selection centered on the original selection midpoint
        center_x = x1 + (width / 2)
        center_y = y1 + (height / 2)
        new_x = int(center_x - (new_width / 2))
        new_y = int(center_y - (new_height / 2))

        return (new_x, new_y, new_width, new_height)
    except Exception as e:
        logger.error(f"Error converting selection to dimensions: {e}")
        return None

#################################################

def black_bar(image, drawable):
    """Create a black bar on a new layer using the current selection.

    The function expects an active non-empty selection. It creates a new
    transparent layer, keeps the current selection as-is, and fills the
    selected area with black on the new layer.
    """
    image.undo_group_start()
    original_selection = None
    try:
        # Save the original selection to a temporary channel
        original_selection = Gimp.Selection.save(image)

        # Get coordinates for the 4:1 black bar shape
        coords = convert_selection_to_dimensions(image, width_by_height="4:1")
        if coords is None:
            return
        
        new_x, new_y, new_width, new_height = coords
        
        # Set the new selection rectangle on the image
        image.select_rectangle(Gimp.ChannelOps.REPLACE, new_x, new_y, new_width, new_height)
        
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
        # Restore original selection (wrapped in try-except so undo_group_end is guaranteed to run)
        if original_selection is not None:
            try:
                image.select_item(Gimp.ChannelOps.REPLACE, original_selection)
                image.remove_channel(original_selection)
            except Exception as e:
                logger.error(f"Failed to restore original selection: {e}")
                
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
