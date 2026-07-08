#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gimp

def black_bar(image, drawable):
    # this function will introduce a black bar in a seperate layer at a selected position, with a selected size and opacity. The user will be able to select the position, size and opacity of the black bar (with defaults & smart values).
    # todos:
    ## default values: mid of image, default size: 1% of image height 3x1 dimensions, default opacity: 100%, color of bar: black, default orientation: horizontal
    
    Gimp.message("Function kk-black-bar is a placeholder.")

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
