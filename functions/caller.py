#!/usr/bin/env python

'''
Helper module to manage imports of awe functions
'''

from functions.accesskeys import accesskeys
from functions.aria_allowed_attr import aria_allowed_attr
from functions.aria_required_attr import aria_required_attr
from functions.aria_required_children import aria_required_children
from functions.aria_required_parent import aria_required_parent
from functions.aria_roles import aria_roles
from functions.aria_valid_attr_value import aria_valid_attr_value
from functions.aria_valid_attr import aria_valid_attr
from functions.audio_caption import audio_caption
from functions.button_name import button_name
from functions.bypass import bypass
from functions.color_contrast import color_contrast
from functions.definition_list import definition_list
from functions.dlitem import dlitem
from functions.document_title import document_title
from functions.duplicate_id import duplicate_id
from functions.frame_title import frame_title
from functions.html_lang_valid import html_lang_valid
from functions.html_lang import html_lang
from functions.image_alt import image_alt
from functions.input_image_alt import input_image_alt
from functions.label import label
from functions.layout_table import layout_table
from functions.link_name import link_name
from functions.list_item import list_item
from functions.par_list import par_list
from functions.meta_refresh import meta_refresh
from functions.meta_viewport import meta_viewport
from functions.object_alt import object_alt
from functions.tab_index import tab_index
from functions.td_headers_attr import td_headers_attr
from functions.th_data_cells import th_data_cells
from functions.valid_lang import valid_lang
from functions.video_caption import video_caption
from functions.video_description import video_description


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

    def run(self, functionName, *args, **kwargs):
        """
        Main method to call each helper function. Just pass the function name
        and any arguments (positional or keyword).

        Parameters:
            functionName <str> Name of the function to run
            args <any> All positional arguments
            kwargs <any> All keyword arguments
        """
        return self.functions[functionName].run(args, kwargs)
