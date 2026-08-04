#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from gi.repository import Gimp, GLib, Gegl
from typing import List, Dict, Any, Optional

logger = logging.getLogger("KonradFilters")

class Base:
    def __init__(self):
        pass

class ImageProcessor(Base):
    def _set_unique_name(self, image: Gimp.Image, item: Any, desired_name: str) -> str:
        """Set a unique name for an image item by appending numbered suffixes.

        If ``desired_name`` already exists in the image, this method uses
        ``"<name> (2)"``, ``"<name> (3)"``, ... until a free name is found.

        Args:
            image (Gimp.Image): The image containing the item.
            item (Any): The item to be renamed (layer/group/drawable).
            desired_name (str): Preferred name.

        Returns:
            str: The effective unique name that was assigned.
        """
        existing_names = set()

        def _collect_names(layer_items: Any) -> None:
            for layer in layer_items or []:
                try:
                    if layer != item:
                        existing_names.add(layer.get_name())
                except Exception:
                    continue
                try:
                    children = layer.get_children()
                except Exception:
                    children = None
                if children:
                    _collect_names(children)

        try:
            _collect_names(image.get_layers())
        except Exception:
            # Best effort: if layers cannot be listed, keep requested name.
            pass

        effective_name = desired_name
        if effective_name in existing_names:
            idx = 2
            while f"{desired_name} ({idx})" in existing_names:
                idx += 1
            effective_name = f"{desired_name} ({idx})"

        item.set_name(effective_name)
        return effective_name

    def _call_pdb(self, proc_name: str, **kwargs) -> Any:
        """Calls a PDB procedure with the given arguments.

        Args:
            proc_name (str): The name of the PDB procedure to call.

        Raises:
            RuntimeError: If the PDB procedure is not found.
            RuntimeError: If the PDB procedure fails to run.


        Returns:
            Any: The result of the PDB procedure.
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

    def _create_solid_filled_layer(
        self,
        image,
        drawable,
        name: str,
        color: str,
        position: int = 0,
        opacity: float = 100.0,
        mode=Gimp.LayerMode.NORMAL,
    ):
        """Create, insert, and solid-fill a full-size layer at a given stack position."""
        layer = Gimp.Layer.new(
            image,
            name,
            image.get_width(),
            image.get_height(),
            drawable.type_with_alpha(),
            opacity,
            mode,
        )
        image.insert_layer(layer, None, position)
        layer.fill(Gimp.FillType.TRANSPARENT)

        Gimp.context_push()
        try:
            Gimp.context_set_foreground(Gegl.Color.new(color))
            layer.edit_fill(Gimp.FillType.FOREGROUND)
        finally:
            Gimp.context_pop()

        return layer

    def _copy_layer(
            self,
            image: Gimp.Image,
            drawable: Gimp.Drawable,
            layer_group: Gimp.GroupLayer,
            name: Optional[str] = None,
            level: Optional[int] = 0
        ) -> Gimp.Layer:
        """Creates a copy of the given drawable and inserts it into the specified layer group.

        Args:
            image (Gimp.Image): The image to which the layer belongs.
            drawable (Gimp.Drawable): The drawable to copy.
            layer_group (Gimp.GroupLayer): The group layer to insert the new layer into.
            name (Optional[str]): The name for the new layer.

        Returns:
            Gimp.Layer: The newly created layer.
        """
        new_layer = drawable.copy()
        desired_name = name if name else _("Copy of ") + drawable.get_name()
        self._set_unique_name(image, new_layer, desired_name)
        image.insert_layer(new_layer, layer_group, level)
        return new_layer

    # --- STATISTICS ENGINE (OPTIMIZATION) ---
    def _get_cached_stats(self, drawable: Gimp.Drawable) -> Dict[str, Any]:
        """Calculate and return histogram-based statistics for a drawable.

        This helper queries GIMP's ``gimp-drawable-histogram`` procedure once
        and returns values used by enhancement steps.

        Args:
            drawable: The source drawable to analyze.

        Returns:
            A dictionary containing:
                - ``mean`` (float): Mean value of the VALUE histogram channel.
                - ``std_dev`` (float): Standard deviation of pixel values.
                - ``median`` (float): Median value of pixel values.
                - ``pixels`` (int): Number of pixels considered.

            If histogram retrieval fails, returns fallback defaults:
            ``{"mean": 127, "std_dev": 0, "median": 127, "pixels": 0}``.
        """
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
    
    def _get_size(self, image: Gimp.Image) -> float:
        """Calculates the size of the image based on its dimensions.

        Args:
            image (Gimp.Image): The image to calculate the size for.

        Returns:
            float: The calculated size.
        """
        return (((image.get_width()**2) + (image.get_height()**2))**0.5)

    def _get_blur_radius(self, size: float) -> float:
        """Calculates a blur radius based on the image size.

        Args:
            size (float): The size of the image.

        Returns:
            float: The calculated blur radius.
        """
        return size / 1000.0

    def _apply_unsharp_mask(
            self,
            drawable: Gimp.Drawable,
            radius: float,
            amount: float,
            threshold: float
        ) -> None:
        """Apply unsharp masking through the GEGL filter backend.

        The legacy PDB procedure ``gimp-drawable-unsharp-mask`` is not
        available in this GIMP3 setup, so we apply ``gegl:unsharp-mask``
        directly on the drawable.
        """
        filt = Gimp.DrawableFilter.new(drawable, "gegl:unsharp-mask", "Unsharp Mask")
        cfg = filt.get_config()
        cfg.set_property("std-dev", radius)
        cfg.set_property("scale", amount)
        cfg.set_property("threshold", threshold)
        drawable.merge_filter(filt)

    def _apply_gaussian_blur(
            self,
            drawable: Gimp.Drawable,
            std_dev_x: float,
            std_dev_y: Optional[float] = None,
            label: str = "Blur"
        ) -> None:
        """Apply a GEGL gaussian blur to a drawable."""
        blur_filter = Gimp.DrawableFilter.new(drawable, "gegl:gaussian-blur", label)
        cfg = blur_filter.get_config()
        cfg.set_property("std-dev-x", std_dev_x)
        cfg.set_property("std-dev-y", std_dev_x if std_dev_y is None else std_dev_y)
        drawable.merge_filter(blur_filter)

    def _get_threshold_value(self, stats: Dict[str, Any]) -> float:
        """Calculates a threshold value based on image statistics.

        Args:
            stats (Dict[str, Any]): A dictionary containing image statistics.

        Returns:
            float: The calculated threshold value.
        """
        return ((stats['mean'] * stats['median'])**0.5) / 255.0
    
    def __init__(self):
        super().__init__()