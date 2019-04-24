#!/usr/bin/env python

"""
Helper module to manage imports of awe function and their pipelined calls.
"""

from engine.functions.accesskeys import accesskeys
from engine.functions.audio_caption import audio_caption
from engine.functions.button_name import button_name
from engine.functions.bypass import bypass
from engine.functions.color_contrast import color_contrast
from engine.functions.definition_list import definition_list
from engine.functions.dlitem import dlitem
from engine.functions.document_title import document_title
from engine.functions.duplicate_id import duplicate_id
from engine.functions.frame_title import frame_title
from engine.functions.html_lang import html_lang
from engine.functions.html_lang_valid import html_lang_valid
from engine.functions.image_alt import image_alt
from engine.functions.input_image_alt import input_image_alt
from engine.functions.label import label
from engine.functions.layout_table import layout_table
from engine.functions.link_name import link_name
from engine.functions.list_item import list_item
from engine.functions.meta_refresh import meta_refresh
from engine.functions.meta_viewport import meta_viewport
from engine.functions.object_alt import object_alt
from engine.functions.tab_index import tab_index
from engine.functions.td_headers_attr import td_headers_attr
from engine.functions.th_data_cells import th_data_cells
from engine.functions.valid_lang import valid_lang
from engine.functions.video_caption import video_caption
from engine.functions.video_description import video_description


functions_mapping = {
    "accesskeys": accesskeys,
    "audio_caption": audio_caption,
    "button_name": button_name,
    "bypass": bypass,
    "color_contrast": color_contrast,
    "definition_list": definition_list,
    "dlitem": dlitem,
    "document_title": document_title,
    "duplicate_id": duplicate_id,
    "frame_title": frame_title,
    "html_lang": html_lang,
    "html_lang_valid": html_lang_valid,
    "image_alt": image_alt,
    "input_image_alt": input_image_alt,
    "label": label,
    "layout_table": layout_table,
    "link_name": link_name,
    "list_item": list_item,
    "meta_refresh": meta_refresh,
    "meta_viewport": meta_viewport,
    "object_alt": object_alt,
    "tab_index": tab_index,
    "td_headers_attr": td_headers_attr,
    "th_data_cells": th_data_cells,
    "valid_lang": valid_lang,
    "video_caption": video_caption,
    "video_description": video_description,
}


def run_pipeline(tag):
    """
    Main method to run each tag through its pipeline.

    Parameters:
        tag <dict> Contains the HTML snippet along with a str list of its pipeline

    Return:
        <dict> The same tag but with the snippet fixed
    """
    return _compose_pipeline(tag["pipeline"])(tag)


def _compose_pipeline(function_names):
    """
    Changes the str list of function names into curried pipeline function
    ['a', 'b', 'c'] -> a.run(b.run(c.run(x)))

    Parameters:
        pipeline <list> List of the function names the snippet must go through

    Return:
        <function> Curried pipelined function calls the snippet will go through
    """
    function_list = tuple(functions_mapping[name] for name in function_names)

    def compose(acc, x, function_list):
        if not function_list:
            return acc.run(x)
        return acc.run(compose(function_list[0], x, function_list[1:]))

    return lambda x: compose(function_list[0], x, function_list[1:])
