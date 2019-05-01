#!/usr/bin/env python

"""Constant list of all AWE API functions."""

# Functions that work by receiving then fixing a faulty HTML tag
INDIRECT_FUNCTIONS = [
    "accesskeys",
    "audio-caption",
    "button-name",
    "bypass",
    "color-contrast",
    "definition-list",
    "dlitem",
    "document-title",
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
]

# Functions that work by directly modifying the original HTML
DIRECT_FUNCTIONS = ["meta-refresh"]

AWE_FUNCTIONS = INDIRECT_FUNCTIONS + DIRECT_FUNCTIONS
