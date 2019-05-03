#!/usr/bin/env python

"""
Helper module to manage imports of awe function and their pipelined calls.
"""

from bs4 import BeautifulSoup

from engine.functions.accesskeys import accesskeys as _accesskeys
from engine.functions.audio_caption import audio_caption as _audio_caption
from engine.functions.button_name import button_name as _button_name
from engine.functions.bypass import bypass as _bypass
from engine.functions.color_contrast import color_contrast as _color_contrast
from engine.functions.definition_list import definition_list as _definition_list
from engine.functions.dlitem import dlitem as _dlitem
from engine.functions.document_title import document_title as _document_title
from engine.functions.duplicate_id import duplicate_id as _duplicate_id
from engine.functions.frame_title import frame_title as _frame_title
from engine.functions.html_lang import html_lang as _html_lang
from engine.functions.html_lang_valid import html_lang_valid as _html_lang_valid
from engine.functions.image_alt import image_alt as _image_alt
from engine.functions.input_image_alt import input_image_alt as _input_image_alt
from engine.functions.label import label as _label
from engine.functions.layout_table import layout_table as _layout_table
from engine.functions.link_name import link_name as _link_name
from engine.functions.list_item import list_item as _list_item
from engine.functions.meta_refresh import meta_refresh as _meta_refresh
from engine.functions.meta_viewport import meta_viewport as _meta_viewport
from engine.functions.object_alt import object_alt as _object_alt
from engine.functions.tab_index import tab_index as _tab_index
from engine.functions.td_headers_attr import td_headers_attr as _td_headers_attr
from engine.functions.th_data_cells import th_data_cells as _th_data_cells
from engine.functions.valid_lang import valid_lang as _valid_lang
from engine.functions.video_caption import video_caption as _video_caption
from engine.functions.video_description import video_description as _video_description


_functions_mapping = {
    "accesskeys": _accesskeys,
    "audio-caption": _audio_caption,
    "button-name": _button_name,
    "bypass": _bypass,
    "color-contrast": _color_contrast,
    "definition-list": _definition_list,
    "dlitem": _dlitem,
    "document-title": _document_title,
    "duplicate-id": _duplicate_id,
    "frame-title": _frame_title,
    "html-lang": _html_lang,
    "html-lang-valid": _html_lang_valid,
    "image-alt": _image_alt,
    "input-image-alt": _input_image_alt,
    "label": _label,
    "layout-table": _layout_table,
    "link-name": _link_name,
    "list-item": _list_item,
    "meta-refresh": _meta_refresh,
    "meta-viewport": _meta_viewport,
    "object-alt": _object_alt,
    "tab-index": _tab_index,
    "td-headers-attr": _td_headers_attr,
    "th-data-cells": _th_data_cells,
    "valid-lang": _valid_lang,
    "video-caption": _video_caption,
    "video-description": _video_description,
}


def run_pipeline(tag):
    """
    Main method to run each tag through its pipeline.

    Parameters:
        tag <dict> Contains the HTML snippet along with a str list of its pipeline

    Return:
        <dict> The same tag but with the snippet fixed
    """
    tag["snippet"] = BeautifulSoup(tag["snippet"], "html.parser").find()
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
    function_list = tuple(_functions_mapping[name] for name in function_names)

    def compose(acc, x, function_list):
        if not function_list:
            return acc.run(x)
        return acc.run(compose(function_list[0], x, function_list[1:]))

    return lambda x: compose(function_list[0], x, function_list[1:])
