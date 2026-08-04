#!/usr/bin/env python3
"""
Anonymiser Module for GIMP 3

Provides centrally-managed anonymisation tools for images:
- Black bars (4:1 ratio) for hiding eyes
- Pixelation for obscuring faces (4:5 ratio) 
- Blur for general area anonymisation

All tools are managed through the Anonymiser class for easy extension
and future UI wizard integration.
"""

import logging
import builtins
from enum import Enum

import gi
from gi.repository import Gimp, Gegl
gi.require_version("Gimp", "3.0")
gi.require_version("Gegl", "0.4")

from . import ImageProcessor


logger = logging.getLogger("Anonymiser")

# Helper translation function if not defined globally
# _ = globals().get("_", lambda x: x)
_ = getattr(builtins, "_", globals().get("_", lambda x: x))


class AnonymisationMethod(Enum):
    """Enumeration of available anonymisation methods."""
    BLACK_BAR = "black_bar"
    PIXELATE = "pixelate"
    BLUR = "blur"


class AnonymisationConfig:
    """Configuration container for anonymisation operations.
    
    This class holds all parameters needed for anonymisation operations,
    making it easy to extend with new options for future UI wizards.
    """
    
    def __init__(
        self,
        method: AnonymisationMethod,
        aspect_ratio: str = "1:1",
        blur_radius: float = 20.0,
        pixel_size: float = 10.0,
        layer_name: str | None = None,
        preserve_selection: bool = True
    ):
        """Initialize anonymisation configuration.
        
        Args:
            method: The anonymisation method to use
            aspect_ratio: Target aspect ratio for black bars (e.g., "4:1")
            blur_radius: Radius for blur operations
            pixel_size: Size of pixels for pixelation
            layer_name: Custom name for the created layer
            preserve_selection: Whether to restore original selection after operation
        """
        self.method = method
        self.aspect_ratio = aspect_ratio
        self.blur_radius = blur_radius
        self.pixel_size = pixel_size
        self.layer_name = layer_name
        self.preserve_selection = preserve_selection

class Anonymiser(ImageProcessor):
    """Central manager for all anonymisation operations.
    
    This class provides a unified interface for applying various anonymisation
    techniques to image selections. It's designed to be easily extensible and
    can be adapted into a UI wizard for more flexible user interaction.
    
    Attributes:
        image: The GIMP image being processed
        drawable: The active drawable/layer
        config: Configuration for the anonymisation operation
    """
    
    def __init__(self, image: Gimp.Image, drawable: Gimp.Drawable, config: AnonymisationConfig | None = None):
        """Initialize the Anonymiser.
        
        Args:
            image: The GIMP image to process
            drawable: The active drawable/layer
            config: Optional configuration; defaults will be used if not provided
        """
        super().__init__()
        self.image = image
        self.drawable = drawable
        self.config = config or AnonymisationConfig(method=AnonymisationMethod.BLACK_BAR)
        self._selection_bounds: tuple[int, int, int, int] | None = None
        self._target_bounds: tuple[int, int, int, int] | None = None
        
    def check_selection(self) -> bool:
        """Check if there is an active selection in the image.
        
        Returns:
            True if a non-empty selection exists, False otherwise
        """
        selection = self.image.get_selection()
        if selection is None:
            logger.warning("No selection object found.")
            return False

        success, non_empty, *_unused = selection.bounds(self.image)
        return success and non_empty
    
    def get_selection_bounds(self) -> tuple[int, int, int, int] | None:
        """Get the bounding box of the current selection.
        
        Returns:
            Tuple of (x, y, width, height) or None if no selection
        """
        selection = self.image.get_selection()
        if selection is None:
            return None
            
        success, non_empty, x1, y1, x2, y2 = selection.bounds(self.image)
        if not success or not non_empty:
            return None
            
        return (x1, y1, x2 - x1, y2 - y1)
    
    def calculate_aspect_ratio_bounds(
        self,
        selection_bounds: tuple[int, int, int, int],
        aspect_ratio: str
    ) -> tuple[int, int, int, int]:
        """Calculate new bounds that fit the target aspect ratio within selection.
        
        Args:
            selection_bounds: Original selection (x, y, width, height)
            aspect_ratio: Target ratio as "width:height" (e.g., "4:1")
            
        Returns:
            Tuple of (new_x, new_y, new_width, new_height) centered in selection
        """
        x, y, width, height = selection_bounds
        
        # Parse aspect ratio
        try:
            width_ratio, height_ratio = map(int, aspect_ratio.split(":"))
            if width_ratio <= 0 or height_ratio <= 0:
                raise ValueError("Aspect ratio components must be positive")
        except (ValueError, AttributeError) as e:
            logger.error(f"Invalid aspect ratio '{aspect_ratio}': {e}")
            return selection_bounds
        
        target_ratio = width_ratio / height_ratio
        selection_ratio = width / height if height != 0 else 0
        
        # Calculate new dimensions to fit aspect ratio within selection
        if selection_ratio >= target_ratio:
            # Selection is wider: constrain by height
            new_height = height
            new_width = round(new_height * target_ratio)
        else:
            # Selection is taller: constrain by width
            new_width = width
            new_height = round(new_width / target_ratio)
        
        # Ensure dimensions are valid
        new_width = max(1, min(new_width, width))
        new_height = max(1, min(new_height, height))
        
        # Center the new bounds within the original selection
        center_x = x + (width / 2)
        center_y = y + (height / 2)
        new_x = int(center_x - (new_width / 2))
        new_y = int(center_y - (new_height / 2))
        
        return (new_x, new_y, new_width, new_height)
    
    def create_layer_from_drawable(self, layer_name: str) -> Gimp.Layer:
        """Create a new layer by duplicating the current drawable.
        
        Args:
            layer_name: Name for the new layer
            
        Returns:
            The newly created layer
            
        Raises:
            RuntimeError: If layer creation fails
        """
        new_layer = self.drawable.copy()
        if new_layer is None:
            raise RuntimeError("Failed to duplicate drawable")
        
        # Set unique name and insert at top
        self._set_unique_name(self.image, new_layer, layer_name)
        self.image.insert_layer(new_layer, None, 0)
        
        return new_layer
    
    def apply_black_bar(self) -> Gimp.Layer:
        """Apply black bar anonymisation to the selection.
        
        Creates a new layer with a black rectangle covering the selection area,
        adjusted to the configured aspect ratio (default 4:1 for eye coverage).
        
        Returns:
            The created layer with the black bar
        """
        # Get and validate selection
        selection_bounds = self.get_selection_bounds()
        if selection_bounds is None:
            raise ValueError("No active selection for black bar. Please select an area first.")

        # 1. Calculate 4:1 aspect ratio bounds
        target_bounds = self.calculate_aspect_ratio_bounds(
            selection_bounds,
            self.config.aspect_ratio
        )
        self._target_bounds = target_bounds
        new_x, new_y, new_width, new_height = target_bounds

        # 2. Select the exact 4:1 target rectangle FIRST
        self.image.select_rectangle(Gimp.ChannelOps.REPLACE, new_x, new_y, new_width, new_height)

        # 3. Create a clean RGBA layer
        layer_name = self.config.layer_name or _("Black Bar")
        new_layer = Gimp.Layer.new(
            self.image,
            layer_name,
            self.image.get_width(),
            self.image.get_height(),
            Gimp.ImageType.RGBA_IMAGE,
            100.0,
            Gimp.LayerMode.NORMAL
        )
        self.image.insert_layer(new_layer, None, 0)

        # 4. Set foreground color to solid black and fill
        Gimp.context_set_foreground(Gegl.Color.new("black"))
        new_layer.edit_fill(Gimp.FillType.FOREGROUND)

        logger.info(f"Created solid black bar layer at ({new_x}, {new_y}) with size {new_width}x{new_height}")
        return new_layer
    
    def apply_pixelate(self) -> Gimp.Layer:
        """Apply pixelation anonymisation to the selection.
        
        Creates a new layer by duplicating the drawable, then applies
        pixelation effect to the selected area.
        
        Returns:
            The created layer with pixelation applied
        """
        # Get selection bounds
        selection_bounds = self.get_selection_bounds()
        if selection_bounds is None:
            raise ValueError("No active selection for pixelation")

        # For pixelate, we can optionally adjust to aspect ratio (e.g., 4:5 for faces)
        # or use the selection as-is
        if self.config.aspect_ratio != "1:1":
            target_bounds = self.calculate_aspect_ratio_bounds(
                selection_bounds,
                self.config.aspect_ratio
            )
            self._target_bounds = target_bounds
            new_x, new_y, new_width, new_height = target_bounds
            self.image.select_rectangle(
                Gimp.ChannelOps.REPLACE,
                new_x, new_y, new_width, new_height
            )
        else:
            self._target_bounds = selection_bounds
            new_x, new_y, new_width, new_height = selection_bounds

        # Duplicate active layer
        layer_name = self.config.layer_name or _("Pixelated")
        new_layer = self.create_layer_from_drawable(layer_name)

        pixel_size = max(1.0, float(self.config.pixel_size))

        try:
            # Apply gegl:pixelize filter
            filter_pix = Gimp.DrawableFilter.new(new_layer, "gegl:pixelize", _("Pixelated"))
            config = filter_pix.get_config()
            config.set_property("size-x", pixel_size)
            config.set_property("size-y", pixel_size)
            
            filter_pix.update()
            new_layer.append_filter(filter_pix)
            new_layer.merge_filter(filter_pix)
            
            logger.info(f"Applied gegl:pixelize with size {pixel_size}")
        except Exception as e:
            logger.error(f"Pixelization operation failed: {e}")
            raise
        finally:
            # Deselect after pixelation
            self.image.select_none()

        # Clear everything outside target rectangle on the duplicated layer
        self.image.select_rectangle(
            Gimp.ChannelOps.REPLACE,
            new_x, new_y, new_width, new_height
        )
        Gimp.Selection.invert(self.image)
        new_layer.edit_clear()
        
        return new_layer

    def apply_blur(self) -> Gimp.Layer:
        """Apply blur anonymisation to the selection.
        
        Creates a new layer by duplicating the drawable, then applies
        Gaussian blur to the selected area.
        
        Returns:
            The created layer with blur applied
        """
        # Get selection bounds
        selection_bounds = self.get_selection_bounds()
        if selection_bounds is None:
            raise ValueError("No active selection for blur")

        self._target_bounds = selection_bounds

        # Duplicate active layer
        layer_name = self.config.layer_name or _("Blurred")
        new_layer = self.create_layer_from_drawable(layer_name)

        blur_radius = max(0.1, float(self.config.blur_radius))

        try:
            # Apply gegl:gaussian-blur filter
            filter_blur = Gimp.DrawableFilter.new(new_layer, "gegl:gaussian-blur", _("Blurred"))
            config = filter_blur.get_config()
            config.set_property("std-dev-x", blur_radius)
            config.set_property("std-dev-y", blur_radius)
            
            filter_blur.update()
            new_layer.append_filter(filter_blur)
            new_layer.merge_filter(filter_blur)  # Merge destructively into new_layer
            
            logger.info(f"Applied gegl:gaussian-blur with radius {blur_radius}")
        except Exception as e:
            logger.error(f"Blur operation failed: {e}")
            raise
        finally:
            # Clear area outside selection on the duplicated layer
            Gimp.Selection.invert(self.image)
            new_layer.edit_clear()
        
        return new_layer
    
    def apply(self) -> Gimp.Layer:
        """Apply the configured anonymisation method.
        
        This is the main entry point for applying anonymisation. It delegates
        to the appropriate method based on the configuration.
        
        Returns:
            The created layer with anonymisation applied
            
        Raises:
            ValueError: If no valid selection exists or method is unknown
        """
        # Validate selection
        if not self.check_selection():
            raise ValueError("No active selection found. Please make a selection first.")
        
        # Store original selection bounds
        self._selection_bounds = self.get_selection_bounds()
        
        # Apply the appropriate method
        if self.config.method == AnonymisationMethod.BLACK_BAR:
            return self.apply_black_bar()
        elif self.config.method == AnonymisationMethod.PIXELATE:
            return self.apply_pixelate()
        elif self.config.method == AnonymisationMethod.BLUR:
            return self.apply_blur()
        else:
            raise ValueError(f"Unknown anonymisation method: {self.config.method}")


#################################################
# Public API Functions
#################################################

def black_bar(image, drawable):
    """Create a black bar (4:1 ratio) on a new layer using the current selection.
    
    This function is designed for quickly hiding eyes in photos. It expects an
    active non-empty selection and creates a black rectangle adjusted to a 4:1
    aspect ratio, centered on the selection.
    
    Args:
        image: The GIMP image
        drawable: The active drawable/layer
    """
    image.undo_group_start()
    original_selection = None
    
    try:
        # Provide a user-friendly exit if there is no active selection.
        selection = image.get_selection()
        if selection is None:
            Gimp.message(_("No active selection. Please select an area first."))
            return

        
        success, non_empty, *_unused = selection.bounds(image)
        if not success or not non_empty:
            Gimp.message(_("No active selection. Please select an area first."))
            return

        # Save the original selection
        original_selection = Gimp.Selection.save(image)
        
        # Configure and apply black bar
        config = AnonymisationConfig(
            method=AnonymisationMethod.BLACK_BAR,
            aspect_ratio="4:1",
            layer_name=_("Black Bar")
        )
        
        anonymiser = Anonymiser(image, drawable, config)
        anonymiser.apply()
        
    except Exception as e:
        logger.exception("Black bar operation failed")
        Gimp.message(f"Error creating black bar: {e}")
    finally:
        # Restore original selection
        if original_selection is not None:
            try:
                image.select_item(Gimp.ChannelOps.REPLACE, original_selection)
                image.remove_channel(original_selection)
            except Exception as e:
                logger.error(f"Failed to restore original selection: {e}")
        
        image.undo_group_end()
    
    Gimp.displays_flush()

def pixelate(image, drawable):
    """Apply pixelation to the current selection.
    
    This function is designed for obscuring faces or other identifiable features.
    It expects an active non-empty selection and applies pixelation to the area,
    optionally adjusting to a 4:5 aspect ratio (portrait orientation).
    
    Args:
        image: The GIMP image
        drawable: The active drawable/layer
    """
    image.undo_group_start()
    original_selection = None
    
    try:
        # Save the original selection
        original_selection = Gimp.Selection.save(image)
        
        # Configure and apply pixelation
        config = AnonymisationConfig(
            method=AnonymisationMethod.PIXELATE,
            aspect_ratio="4:5",  # Portrait ratio for faces
            pixel_size=10.0,
            layer_name=_("Pixelated")
        )
        
        anonymiser = Anonymiser(image, drawable, config)
        anonymiser.apply()
        
    except Exception as e:
        logger.error(f"Pixelation operation failed: {e}")
        Gimp.message(f"Error applying pixelation: {e}")
    finally:
        # Restore original selection
        if original_selection is not None:
            try:
                image.select_item(Gimp.ChannelOps.REPLACE, original_selection)
                image.remove_channel(original_selection)
            except Exception as e:
                logger.error(f"Failed to restore original selection: {e}")
        
        image.undo_group_end()
    
    Gimp.displays_flush()


def blur(image, drawable):
    """Apply blur to the current selection.
    
    This function applies Gaussian blur to the selected area for general
    anonymisation purposes. It preserves the original selection shape.
    
    Args:
        image: The GIMP image
        drawable: The active drawable/layer
    """
    image.undo_group_start()
    original_selection = None
    
    try:
        # Save the original selection
        original_selection = Gimp.Selection.save(image)
        
        # Configure and apply blur
        config = AnonymisationConfig(
            method=AnonymisationMethod.BLUR,
            aspect_ratio="1:1",  # Keep original selection shape
            blur_radius=20.0,
            layer_name=_("Blurred")
        )
        
        anonymiser = Anonymiser(image, drawable, config)
        anonymiser.apply()
        
    except Exception as e:
        logger.error(f"Blur operation failed: {e}")
        Gimp.message(f"Error applying blur: {e}")
    finally:
        # Restore original selection
        if original_selection is not None:
            try:
                image.select_item(Gimp.ChannelOps.REPLACE, original_selection)
                image.remove_channel(original_selection)
            except Exception as e:
                logger.error(f"Failed to restore original selection: {e}")
        
        image.undo_group_end()
    
    Gimp.displays_flush()


def anonymise_custom(
    image,
    drawable,
    method: str = "black_bar",
    aspect_ratio: str = "4:1",
    blur_radius: float = 20.0,
    pixel_size: float = 10.0,
    layer_name: str | None = None
):
    """Apply custom anonymisation with flexible parameters.
    
    This function provides a flexible interface for anonymisation operations,
    allowing full control over all parameters. It's designed to be easily
    integrated into a UI wizard.
    
    Args:
        image: The GIMP image
        drawable: The active drawable/layer
        method: Anonymisation method ("black_bar", "pixelate", or "blur")
        aspect_ratio: Target aspect ratio as "width:height"
        blur_radius: Radius for blur operations
        pixel_size: Size of pixels for pixelation
        layer_name: Custom name for the created layer
    """
    image.undo_group_start()
    original_selection = None
    
    try:
        # Save the original selection
        original_selection = Gimp.Selection.save(image)
        
        # Parse method
        method_map = {
            "black_bar": AnonymisationMethod.BLACK_BAR,
            "pixelate": AnonymisationMethod.PIXELATE,
            "blur": AnonymisationMethod.BLUR
        }
        
        anonymisation_method = method_map.get(method.lower())
        if anonymisation_method is None:
            raise ValueError(f"Unknown method: {method}. Use 'black_bar', 'pixelate', or 'blur'")
        
        # Configure and apply
        config = AnonymisationConfig(
            method=anonymisation_method,
            aspect_ratio=aspect_ratio,
            blur_radius=blur_radius,
            pixel_size=pixel_size,
            layer_name=layer_name
        )
        
        anonymiser = Anonymiser(image, drawable, config)
        anonymiser.apply()
        
    except Exception as e:
        logger.error(f"Custom anonymisation failed: {e}")
        Gimp.message(f"Error applying anonymisation: {e}")
    finally:
        # Restore original selection
        if original_selection is not None:
            try:
                image.select_item(Gimp.ChannelOps.REPLACE, original_selection)
                image.remove_channel(original_selection)
            except Exception as e:
                logger.error(f"Failed to restore original selection: {e}")
        
        image.undo_group_end()
    
    Gimp.displays_flush()


# Backwards-compatible aliases used by existing plugin registrations.
def pixeled(image, drawable):
    """Legacy alias for pixelate()."""
    return pixelate(image, drawable)


def blurred(image, drawable):
    """Legacy alias for blur()."""
    return blur(image, drawable)
