#!/usr/bin/env python

"""
Main class for the Accessibility Web Engine.

Holds the true copies of the target page HTML as well as the parsed Lighthouse
Audit results. AWE then segments and distributes these files to the concerned
accessibility functions.

Finally, it reassembles the function outputs into the accessible version of the
target site.
"""

# TODO
# from .crawler import HTMLCrawler
# from lighthouse import lighthouseAuditer

from .functions import Caller as AWECaller
from .lighthouse import Lighthouse
from . import constants


class Engine:
    """
    Main entry point for AWE.
    Manages calls to accessibility functions and reassembles the site into its
    more accessible version.

    Parameters:
        site_html <str> The HTML code of the target site
    """

    def __init__(
        self,
        *,
        target_url,
        audit_format="json",
        site_html=None,
    ):
        self.target_url = target_url
        self._audit_format = audit_format
        self._site_html = site_html

        self._lighthouse = Lighthouse(
            function_names=constants.AWE_FUNCTIONS,
            target_url=target_url,
            audit_format=audit_format,
        )

    def get_full_audit_data(self):
        """Wrapper around lighthouse audit to return the full parsed audit"""
        return self._lighthouse.get_audit_data()

    def run_analysis(self, force=False):
        self._lighthouse.run(force)

    def run_engine(self):
        """
        Organizes function calls sending them the proper HTML and Audit data.
        Accessibility functions receive a dictionary with keys ["colors", "selector",
        "snippet"].

        The color key contains the foreground and background colors for the
        color-contrast function only. Empty object for others.

        selector is the css selector for the tag.

        snippet is the failing HTML tag as a string.
        """
        awe_caller = AWECaller()

        result = {}

        for functionName in constants.AWE_FUNCTIONS:
            functionData = self._lighthouse.get_audit_data(functionName)

            if functionData["failing"] and functionData["applicable"]:
                result[functionName] = awe_caller.run(
                    name=functionName, failingItems=functionData["items"]
                )

        return result

    def reassemble_site(self):
        """
        Recombines the site's HTML into a more accessible version by replacing
        the offending code with the output of the corresponding AWE function.
        """
        pass
