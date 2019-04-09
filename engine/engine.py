#!/usr/bin/env python3

"""
Main class for the Accessibility Web Engine.

Holds the true copies of the target page HTML as well as the parsed Lighthouse
Audit results. AWE then segments and distributes these files to the concerned
accessibility functions.

Finally, it reassembles the function outputs into the accessible version of the
target site.
"""


from . import constants
from .crawler import Crawler
from .functions import Caller as AWECaller
from .lighthouse import Lighthouse


class Engine:
    """
    Main entry point for AWE.
    Manages calls to accessibility functions and reassembles the site into its
    more accessible version.

    Parameters:
        site_html <str> The HTML code of the target site
    """

    def __init__(self, *, target_url, audit_format="json"):
        self.target_url = target_url
        self._audit_format = audit_format

        self._crawler = Crawler(target_url=self.target_url)

        self._lighthouse = Lighthouse(
            function_names=constants.AWE_FUNCTIONS,
            target_url=target_url,
            audit_format=audit_format,
        )

    def run_analysis(self, force=False):
        """
        Runs a lighthouse analysis on the site.

        Parameters:
            force <bool> Force a rerun of the analysis
        """
        self._lighthouse.run(force)

    def get_full_audit_data(self):
        """Get the full parsed audit"""
        return self._lighthouse.get_audit_data()

    async def run_crawler(self, force=False):
        """
        Crawls the site and scrapes the HTML.

        Parameters:
            force <bool> Force a rerun of the crawl
        """
        await self._crawler.crawl(force)

    def get_html(self):
        """Get the crawled html of the site."""
        return self._crawler.get_raw_html()

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
