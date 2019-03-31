#!/usr/bin/env python

"""
Helper module to manage imports of awe functions.
"""

from awe.functions.accesskeys import accesskeys
from awe.functions.aria_allowed_attr import aria_allowed_attr
from awe.functions.aria_required_attr import aria_required_attr
from awe.functions.aria_required_children import aria_required_children
from awe.functions.aria_required_parent import aria_required_parent
from awe.functions.aria_roles import aria_roles
from awe.functions.aria_valid_attr_value import aria_valid_attr_value
from awe.functions.aria_valid_attr import aria_valid_attr
from awe.functions.audio_caption import audio_caption
from awe.functions.button_name import button_name
from awe.functions.bypass import bypass
from awe.functions.color_contrast import color_contrast
from awe.functions.definition_list import definition_list
from awe.functions.dlitem import dlitem
from awe.functions.document_title import document_title
from awe.functions.duplicate_id import duplicate_id
from awe.functions.frame_title import frame_title
from awe.functions.html_lang_valid import html_lang_valid
from awe.functions.html_lang import html_lang
from awe.functions.image_alt import image_alt
from awe.functions.input_image_alt import input_image_alt
from awe.functions.label import label
from awe.functions.layout_table import layout_table
from awe.functions.link_name import link_name
from awe.functions.list_item import list_item
from awe.functions.par_list import par_list
from awe.functions.meta_refresh import meta_refresh
from awe.functions.meta_viewport import meta_viewport
from awe.functions.object_alt import object_alt
from awe.functions.tab_index import tab_index
from awe.functions.td_headers_attr import td_headers_attr
from awe.functions.th_data_cells import th_data_cells
from awe.functions.valid_lang import valid_lang
from awe.functions.video_caption import video_caption
from awe.functions.video_description import video_description


class Caller:
    """
    Caller is a helper class meant to offer a single entry point to call all
    awe functions.

    Attributes:
        functions <dict> Mapping of string function name to imported function
    """

    functions = {
        "accesskeys": accesskeys,
        "aria_allowed_attr": aria_allowed_attr,
        "aria_required_attr": aria_required_attr,
        "aria_required_children": aria_required_children,
        "aria_required_parent": aria_required_parent,
        "aria_roles": aria_roles,
        "aria_valid_attr_value": aria_valid_attr_value,
        "aria_valid_attr": aria_valid_attr,
        "audio_caption": audio_caption,
        "button_name": button_name,
        "bypass": bypass,
        "color_contrast": color_contrast,
        "definition_list": definition_list,
        "dlitem": dlitem,
        "document_title": document_title,
        "duplicate_id": duplicate_id,
        "frame_title": frame_title,
        "html_lang_valid": html_lang_valid,
        "html_lang": html_lang,
        "image_alt": image_alt,
        "input_image_alt": input_image_alt,
        "label": label,
        "layout_table": layout_table,
        "link_name": link_name,
        "list_item": list_item,
        "par_list": par_list,
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

    def run(self, *, name, failingItems):
        """
        Main method to call each helper function. Just pass the function name
        and any arguments (positional or keyword).

        Parameters:
            name <str> Name of the function to run
            failingItems <list> Elements that fail 'name' function tests
        """
        return self.functions[name].run(failingItems)
