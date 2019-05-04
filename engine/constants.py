#!/usr/bin/env python

"""Constant list of all AWE API functions."""

from collections import namedtuple

FunctionsList = namedtuple("FUNCTIONS", ["INDIRECT", "DIRECT", "ALL"])

# Functions that work by receiving then fixing a faulty HTML tag
INDIRECT_FUNCTIONS = (
    "accesskeys",
    "audio-caption",
    "button-name",
    "bypass",
    "color-contrast",
    "definition-list",
    "dlitem",
    "duplicate-id",
    "frame-title",
    "html-lang",
    "html-lang-valid",
    "image-alt",
    "input-image-alt",
    "label",
    "layout-table",
    "link-name",
    "list",
    "listitem",
    "meta-viewport",
    "object-alt",
    "tab-index",
    "td-headers-attr",
    "th-has-data-cells",
    "valid-lang",
    "video-caption",
    "video-description",
)

# Functions that work by directly modifying the original HTML
DIRECT_FUNCTIONS = ("document-title", "meta-refresh", "dlitem", "frame_title")

AWE_FUNCTIONS = FunctionsList(
    INDIRECT_FUNCTIONS, DIRECT_FUNCTIONS, INDIRECT_FUNCTIONS + DIRECT_FUNCTIONS
)
