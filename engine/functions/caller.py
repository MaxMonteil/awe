#!/usr/bin/env python

"""
Helper module to manage imports of awe functions.
"""

from engine.functions.accesskeys import accesskeys
from engine.functions.aria_allowed_attr import aria_allowed_attr
from engine.functions.aria_required_attr import aria_required_attr
from engine.functions.aria_required_children import aria_required_children
from engine.functions.aria_required_parent import aria_required_parent
from engine.functions.aria_roles import aria_roles
from engine.functions.aria_valid_attr_value import aria_valid_attr_value
from engine.functions.aria_valid_attr import aria_valid_attr
from engine.functions.audio_caption import audio_caption
from engine.functions.button_name import button_name
from engine.functions.bypass import bypass
from engine.functions.color_contrast import color_contrast
from engine.functions.definition_list import definition_list
from engine.functions.dlitem import dlitem
from engine.functions.document_title import document_title
from engine.functions.duplicate_id import duplicate_id
from engine.functions.frame_title import frame_title
from engine.functions.html_lang_valid import html_lang_valid
from engine.functions.html_lang import html_lang
from engine.functions.image_alt import image_alt
from engine.functions.input_image_alt import input_image_alt
from engine.functions.label import label
from engine.functions.layout_table import layout_table
from engine.functions.link_name import link_name
from engine.functions.list_item import list_item
from engine.functions.par_list import par_list
from engine.functions.meta_refresh import meta_refresh
from engine.functions.meta_viewport import meta_viewport
from engine.functions.object_alt import object_alt
from engine.functions.tab_index import tab_index
from engine.functions.td_headers_attr import td_headers_attr
from engine.functions.th_data_cells import th_data_cells
from engine.functions.valid_lang import valid_lang
from engine.functions.video_caption import video_caption
from engine.functions.video_description import video_description


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

    def run_pipeline(self, tag):
        """
        Main method to run each tag through its pipeline.

        Parameters:
            tag <dict> Contains the HTML snippet along with a str list of its pipeline

        Return:
            <dict> The same tag but with the snippet fixed
        """
        return self._compose_pipeline(tag["pipeline"])(tag)

    def _compose_pipeline(self, pipeline):
        """
        Changes the str list of function names into curried pipeline function
        ['a', 'b', 'c'] -> a.run(b.run(c.run(x)))

        Parameters:
            pipeline <list> List of the function names the snippet must go through

        Return:
            <function> Curried pipelined function calls the snippet will go through
        """
        if len(pipeline) == 1:
            return lambda x: self.functions[pipeline[0]].run(x)

        return self.functions[pipeline[0]].run(self._compose_pipeline(pipeline[1:]))
