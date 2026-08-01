#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from . import ImageProcessor
from gi.repository import Gimp, GLib
from typing import List, Dict, Any, Optional

logger = logging.getLogger("Anonymiser")

# Helper translation function if not defined globally
try:
    _
except NameError:
    _ = lambda x: x


#################################################

def _duplicate_blur_pixelate_and_crop(image, drawable, coords, blur_radius):
    """Duplicate drawable, apply blur+pixelate, and keep only coords area."""
    new_x, new_y, new_width, new_height = coords

    edited_layer = drawable.copy()
    if edited_layer is None:
        raise RuntimeError("Could not duplicate drawable.")

    edited_layer.set_name(_("Anonymised"))
    image.insert_layer(edited_layer, None, 0)

    half_blur = max(0.1, float(blur_radius) / 2.0)
    pixel_size = max(1.0, float(blur_radius) * 10.0)

    pdb = Gimp.get_pdb()
    pdb.run_procedure(
        "plug-in-gauss",
        [
            Gimp.RunMode.NONINTERACTIVE,
            image,
            edited_layer,
            half_blur,
            half_blur,
            0,
        ],
    )

    pixelized = False
    try:
        pdb.run_procedure(
            "plug-in-pixelize2",
            [
                Gimp.RunMode.NONINTERACTIVE,
                image,
                edited_layer,
                pixel_size,
                pixel_size,
            ],
        )
        pixelized = True
    except Exception:
        pass

    if not pixelized:
        pdb.run_procedure(
            "plug-in-pixelize",
            [
                Gimp.RunMode.NONINTERACTIVE,
                image,
                edited_layer,
                pixel_size,
            ],
        )

    image.select_rectangle(Gimp.ChannelOps.REPLACE, new_x, new_y, new_width, new_height)
    Gimp.Selection.invert(image)
    edited_layer.edit_clear()
    Gimp.Selection.none(image)

def black_bar(image, drawable):
    """Create a black bar on a new layer using the current selection.
    
    The function expects an active non-empty selection. It creates a new
    transparent layer, keeps the current selection as-is, and fills the
    selected area with black on the new layer.
    """
    image.undo_group_start()
    operation = Anonymiser(image, drawable)
    original_selection = None
    
    try:
        # Save the original selection to a temporary channel
        original_selection = Gimp.Selection.save(image)
        ### Mockup for black bar creation logic
        operation.determine_bar_selection()
        operation.create_black_bar_layer()

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

def __legacy__black_bar(image, drawable):
    """Create a black bar on a new layer using the current selection.

    The function expects an active non-empty selection. It creates a new
    transparent layer, keeps the current selection as-is, and fills the
    selected area with black on the new layer.
    """
    image.undo_group_start()
    operation = Anonymiser(image, drawable)
    original_selection = None
    
    try:
        # Save the original selection to a temporary channel
        original_selection = Gimp.Selection.save(image)

        # Get coordinates for the 4:1 black bar shape
        coords = operation.convert_selection_to_dimensions(image, width_by_height="4:1")
        if coords is None:
            return
        
        new_x, new_y, new_width, new_height = coords
        
        # Set the new selection rectangle on the image
        image.select_rectangle(Gimp.ChannelOps.REPLACE, new_x, new_y, new_width, new_height)
        
        blur_radius = getattr(operation, "blur_radius", 10.0)
        _duplicate_blur_pixelate_and_crop(
            image,
            drawable,
            (new_x, new_y, new_width, new_height),
            blur_radius,
        )

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
    """Create a black bar on a new layer using the current selection.

    The function expects an active non-empty selection. It creates a new
    transparent layer, keeps the current selection as-is, and fills the
    selected area with black on the new layer.
    """
    image.undo_group_start()
    operation = Anonymiser(image, drawable)
    original_selection = None

    try:
        # Save the original selection to a temporary channel
        original_selection = Gimp.Selection.save(image)
        
        ### Mockup for pixeled creation logic
        operation.determine_pixel_selection()
        operation.create_pixelated_layer()

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

def __legacy__pixeled(image, drawable):
    """Create a black bar on a new layer using the current selection.

    The function expects an active non-empty selection. It creates a new
    transparent layer, keeps the current selection as-is, and fills the
    selected area with black on the new layer.
    """
    image.undo_group_start()
    operation = Anonymiser(image, drawable)
    original_selection = None
    
    
    try:
        # Save the original selection to a temporary channel
        original_selection = Gimp.Selection.save(image)

        # Get coordinates for the 4:1 black bar shape
        coords = operation.convert_selection_to_dimensions(image, width_by_height="4:5")
        if coords is None:
            return
        
        new_x, new_y, new_width, new_height = coords
        
        # Set the new selection rectangle on the image
        image.select_rectangle(Gimp.ChannelOps.REPLACE, new_x, new_y, new_width, new_height)
        
        blur_radius = getattr(operation, "blur_radius", 10.0)
        _duplicate_blur_pixelate_and_crop(
            image,
            drawable,
            (new_x, new_y, new_width, new_height),
            blur_radius,
        )

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

def blurred(image, drawable):
    """Create a black bar on a new layer using the current selection.

    The function expects an active non-empty selection. It creates a new
    transparent layer, keeps the current selection as-is, and fills the
    selected area with black on the new layer.
    """
    image.undo_group_start()
    operation = Anonymiser(image, drawable)
    original_selection = None

    try:
        # Save the original selection to a temporary channel
        original_selection = Gimp.Selection.save(image)
        
        ### Mockup for pixeled creation logic
        operation.determine_blurred_selection()
        operation.create_blurred_layer()

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


class Anonymiser(ImageProcessor):
    
    def check_selection(self, drawable: Gimp.Drawable) -> bool:
        """Check if there is an active selection in the drawable."""
        has_selection, _, _, _, _ = drawable.mask_intersect()
        return has_selection
    
    def convert_selection_to_dimensions(
            self,
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
            if width_ratio <= 0 or height_ratio <= 0:
                logger.warning("Invalid width_by_height ratio provided.")
                return None

            target_ratio = width_ratio / height_ratio
            selection_ratio = width / height if height != 0 else 0

            # Keep requested ratio and fit it inside the current selection bounds
            if selection_ratio >= target_ratio:
                # Selection is wider than target ratio: use full height
                new_height = height
                new_width = int(round(new_height * target_ratio))
            else:
                # Selection is taller/narrower than target ratio: use full width
                new_width = width
                new_height = int(round(new_width / target_ratio))

            new_width = max(1, min(new_width, width))
            new_height = max(1, min(new_height, height))
            
            # Keep the new selection centered on the original selection midpoint
            center_x = x1 + (width / 2)
            center_y = y1 + (height / 2)
            new_x = int(center_x - (new_width / 2))
            new_y = int(center_y - (new_height / 2))

            return (new_x, new_y, new_width, new_height)
        except Exception as e:
            logger.error(f"Error converting selection to dimensions: {e}")
            return None 
    
    def determine_bar_selection(self):
        """Determine the selection for the black bar based on the current selection."""
        # Placeholder logic for determining black bar selection
        logger.info("Determining black bar selection (placeholder).")
        # Actual implementation would analyze the current selection and set parameters accordingly.
    def create_black_bar_layer(self):
        """Create a black bar layer based on the determined selection."""
        # Placeholder logic for creating black bar layer
        logger.info("Creating black bar layer (placeholder).")
        # Actual implementation would create a new layer and fill the determined selection area with black.
    def determine_pixel_selection(self):
        """Determine the selection for pixelation based on the current selection."""
        # Placeholder logic for determining pixelation selection
        logger.info("Determining pixelation selection (placeholder).")
        # Actual implementation would analyze the current selection and set parameters accordingly.
    def create_pixelated_layer(self):
        """Create a pixelated layer based on the determined selection."""
        # Placeholder logic for creating pixelated layer
        logger.info("Creating pixelated layer (placeholder).")
        # Actual implementation would create a new layer and apply pixelation to the determined selection area.
    def determine_blurred_selection(self):
        """Determine the selection for blurring based on the current selection."""
        # Placeholder logic for determining blurred selection
        logger.info("Determining blurred selection (placeholder).")
        # Actual implementation would analyze the current selection and set parameters accordingly.
    def create_blurred_layer(self):
        """Create a blurred layer based on the determined selection."""
        # Placeholder logic for creating blurred layer
        logger.info("Creating blurred layer (placeholder).")
        # Actual implementation would create a new layer and apply blurring to the determined selection area.

    def __init__(self, image, drawable):
        Gimp.message("Function kk-anonymiser is a placeholder.")
        super().__init__()
