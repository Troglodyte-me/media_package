#!/usr/bin/env python
# Copyright (c) 2026 Troglodyte-me
# This software is released under the GNU GPL v3.0 under https://github.com/Troglodyte-me/media_package
# See LICENSE file in the repository root for full details.

# Tutorial available at: https://www.youtube.com/watch?v=nmb-0KcgXzI
# Feedback welcome: jacksonbates@hotmail.com

from gimpfu import *
from datetime import datetime
#import statistics

LAYER_MODE = { 
    "NORMAL-LEGACY": 0, 
    "DISSOLVE": 1, 
    "BEHIND-LEGACY": 2, 
    "MULTIPLY-LEGACY": 3, 
    "SCREEN-LEGACY": 4, 
    "OVERLAY-LEGACY": 5, 
    "DIFFERENCE-LEGACY": 6, 
    "ADDITION-LEGACY": 7, 
    "SUBTRACT-LEGACY": 8, 
    "DARKEN-ONLY-LEGACY": 9, 
    "LIGHTEN-ONLY-LEGACY": 10, 
    "HSV-HUE-LEGACY": 11, 
    "HSV-SATURATION-LEGACY": 12, 
    "HSL-COLOR-LEGACY": 13, 
    "HSV-VALUE-LEGACY": 14, 
    "DIVIDE-LEGACY": 15, 
    "DODGE-LEGACY": 16, 
    "BURN-LEGACY": 17, 
    "HARDLIGHT-LEGACY": 18, 
    "SOFTLIGHT-LEGACY": 19, 
    "GRAIN-EXTRACT-LEGACY": 20, 
    "GRAIN-MERGE-LEGACY": 21, 
    "COLOR-ERASE-LEGACY": 22, 
    "OVERLAY": 23, 
    "LCH-HUE": 24, 
    "LCH-CHROMA": 25, 
    "LCH-COLOR": 26, 
    "LCH-LIGHTNESS": 27, 
    "NORMAL": 28, 
    "BEHIND": 29, 
    "MULTIPLY": 30, 
    "SCREEN": 31, 
    "DIFFERENCE": 32, 
    "ADDITION": 33, 
    "SUBTRACT": 34, 
    "DARKEN-ONLY": 35, 
    "LIGHTEN-ONLY": 36, 
    "HSV-HUE": 37, 
    "HSV-SATURATION": 38, 
    "HSL-COLOR": 39, 
    "HSV-VALUE": 40, 
    "DIVIDE": 41, 
    "DODGE": 42, 
    "BURN": 43, 
    "HARDLIGHT": 44, 
    "SOFTLIGHT": 45, 
    "GRAIN-EXTRACT": 46, 
    "GRAIN-MERGE": 47, 
    "VIVID-LIGHT": 48, 
    "PIN-LIGHT": 49, 
    "LINEAR-LIGHT": 50, 
    "HARD-MIX": 51, 
    "EXCLUSION": 52, 
    "LINEAR-BURN": 53, 
    "LUMA-DARKEN-ONLY": 54, 
    "LUMA-LIGHTEN-ONLY": 55, 
    "LUMINANCE": 56, 
    "COLOR-ERASE": 57, 
    "ERASE": 58, 
    "MERGE": 59, 
    "SPLIT": 60, 
    "PASS-THROUGH": 61, 
    "REPLACE": 62, 
    "ANTI-ERASE": 63
    }
    
def alter_brightness_contrast(drawable, brightness, contrast):
    if brightness > 1.0 or contrast > 1.0:
        brightness = ( float(brightness)/(256.0/2.0) ) / 2.0
        contrast = ( float(contrast)/(256.0/2.0) ) / 2.0
    return pdb.gimp_drawable_brightness_contrast(drawable, brightness, contrast)

def get_avg_threshold(drawable, channel, start_range, end_range):
    mean, std_dev, median, pixels, count, percentile = pdb.gimp_drawable_histogram(
        drawable, 
        channel, 
        start_range, 
        end_range
    )
    return ((mean*median) ** (1.0/2.0)) / 255.0

def alter_color_threshold(drawable, channel = 0):
    threshold = get_avg_threshold(drawable, channel, 0, 1)
    return pdb.gimp_drawable_threshold(
        drawable, 
        channel, 
        threshold,
        1.0
    )

def avg_item_size(image):
    return ( float(image.width * image.height) ** (1.0/2.0) )

def alter_blur(image, drawable, px):
    return pdb.plug_in_gauss(image, drawable, px, px, .5)


def Enhance_Image(image, drawable):
    now = datetime.now()
    # pdb.gimp_message( now.strftime("%d/%m/%Y %H:%M:%S") )
    img_threshold = get_avg_threshold(drawable, 0, 0, 1)
    size = avg_item_size(image)

    ## create layers (stag backwards)
    orig_name = str(drawable.name)
    drawable.name = 'original'
    
    main_layer_group = pdb.gimp_layer_group_new(image)
    pdb.gimp_image_insert_layer(image, main_layer_group, None, 0)
    main_layer_group.name = orig_name
    pdb.gimp_image_reorder_item(image, drawable, main_layer_group, 0)
    
    white_balance = pdb.gimp_layer_new_from_drawable(drawable, image)
    white_balance.name = 'white balance'
    pdb.gimp_image_insert_layer(image, white_balance, main_layer_group, 0)
    white_balance.opacity = 90.0
    # white_balance.mode = LAYER_MODE['NORMAL']
    
    grey_layer_group = pdb.gimp_layer_group_new(image)
    grey_layer_group.name = 'grayscale'
    pdb.gimp_image_insert_layer(image, grey_layer_group, main_layer_group, 0)
    grey_layer_group.opacity = 10.0
    grey_layer_group.mode = LAYER_MODE['MULTIPLY']
    
    equalize = pdb.gimp_layer_new_from_drawable(drawable, image)
    equalize.name = 'equalize'
    pdb.gimp_image_insert_layer(image, equalize, main_layer_group, 0)
    equalize.opacity = 25.0
    if img_threshold > 0.5:
        equalize.mode = LAYER_MODE['OVERLAY']
    else:
        equalize.mode = LAYER_MODE['SCREEN']
    
    white_balance_grey = pdb.gimp_layer_new_from_drawable(drawable, image)
    white_balance_grey.name = 'grey by white balance'
    pdb.gimp_image_insert_layer(image, white_balance_grey, grey_layer_group, 0)
    # white_balance_grey.opacity = 100.0
    # equalize.mode = LAYER_MODE['NORMAL']
    
    white_balance_bw = pdb.gimp_layer_new_from_drawable(drawable, image)
    white_balance_bw.name = 'b/w by white balance (incl blur)'
    pdb.gimp_image_insert_layer(image, white_balance_bw, grey_layer_group, 0)
    white_balance_bw.opacity = 10.0
    # equalize.mode = LAYER_MODE['NORMAL']
    
    equalize_grey = pdb.gimp_layer_new_from_drawable(drawable, image)
    equalize_grey.name = 'grey by equalize'
    pdb.gimp_image_insert_layer(image, equalize_grey, grey_layer_group, 0)
    equalize_grey.opacity = 50.0
    # equalize.mode = LAYER_MODE['NORMAL']
    
    equalize_bw = pdb.gimp_layer_new_from_drawable(drawable, image)
    equalize_bw.name = 'b/w by equalize (incl bright+contrast)'
    pdb.gimp_image_insert_layer(image, equalize_bw, grey_layer_group, 0)
    equalize_bw.opacity = 10.0
    # equalize.mode = LAYER_MODE['NORMAL']
    
    # pdb.gimp_message( 'all layers created' )


    ## alter layers
    pdb.gimp_drawable_levels_stretch(white_balance)
    # pdb.gimp_message( 'white_balance ready' )
    
    alter_blur(image, white_balance_bw, (size / 1000.0) )
    pdb.gimp_drawable_levels_stretch(white_balance_bw)
    alter_color_threshold(white_balance_bw)
    # pdb.gimp_message( 'white_balance_bw ready' )
    
    alter_brightness_contrast(equalize_bw, 25, 10)
    pdb.gimp_drawable_equalize(equalize_bw, False)
    alter_color_threshold(equalize_bw)
    # pdb.gimp_message( 'equalize_bw ready' )
    
    alter_blur(image, equalize, (size / 1000.0) )
    pdb.gimp_drawable_equalize(equalize, False)
    # pdb.gimp_message( 'equalize ready' )
    
    pdb.gimp_drawable_levels_stretch(white_balance_grey)
    pdb.gimp_drawable_desaturate(white_balance_grey, 0)
    # pdb.gimp_message( 'white_balance_grey ready' )
    
    pdb.gimp_drawable_equalize(equalize_grey, False)
    pdb.gimp_drawable_desaturate(equalize_grey, 0)
    # pdb.gimp_message( 'equalize_grey ready' )
    

register(
    "python-fu-Enhance-Image",
    "ImageEnhancementLayers",
    "Enhance Image by creating some default Layers",
    "Konrad Keck", "Konrad Keck", "2021",
    "create image enhancement layers",
    "RGB*", # type of image it works on (*, RGB, RGB*, RGBA, grey etc...)
    [
        # basic parameters are: (UI_ELEMENT, "variable", "label", Default)
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None)
        # PF_SLIDER, SPINNER have an extra tuple (min, max, step)
        # PF_RADIO has an extra tuples within a tuple:
        # eg. (("radio_label", "radio_value), ...) for as many radio buttons
        # PF_OPTION has an extra tuple containing options in drop-down list
        # eg. ("opt1", "opt2", ...) for as many options
        # see ui_examples_1.py and ui_examples_2.py for live examples
    ],
    [],
    Enhance_Image, menu="<Image>/Filters/Custom")  # second item is menu location

main()