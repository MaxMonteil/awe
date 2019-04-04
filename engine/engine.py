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
from .lighthouseparser import ResponseParser
from . import constants
from bs4 import BeautifulSoup


class Engine:
    """
    Main entry point for AWE.
    Manages calls to accessibility functions and reassembles the site into its
    more accessible version.

    Parameters:
        site_html <str> The HTML code of the target site
        audit_data <str> The resulting audit from running Google Lighthouse on
                         the target site.
    """

    def __init__(self, *, site_html, audit_data):
        self.site_html = site_html

        # Parse result of audit
        self.lhAudit = ResponseParser(
            lighthouseResponse=audit_data, functionNames=constants.AWE_FUNCTIONS
        )

        self.lhAudit.parse_audit_data()

    def run_engine(self):
        """
        Organizes function calls sending them the proper HTML string list.

        Parameters:
            lhAudit <ResponseParser> Parser object with the parsed audit
        """
        awe_caller = AWECaller()

        result = {}

        for functionName in constants.AWE_FUNCTIONS:
            functionData = self.lhAudit.get_audit_data(functionName)

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
