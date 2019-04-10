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
from .functions import Caller
from .lighthouse import Lighthouse
import asyncio


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

    async def run_analysis(self, force=False):
        """
        Runs a lighthouse analysis on the site.

        Parameters:
            force <bool> Force a rerun of the analysis
        """
        await self._lighthouse.run(force)

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
        return self._reassemble_site(asyncio.run(self._run_functions()))

    async def _run_functions(self):
        """
        Organizes function calls sending them the proper HTML and Audit data.
        Accessibility functions receive a dictionary with keys:
        ["colors", "selector", "snippet", "path"]

        The color key contains the foreground and background colors for the
        color-contrast function only. Empty object for others.

        selector is the css selector for the tag.

        snippet is the failing HTML tag as a string.

        path is the HTML tree path to the snippet
        """
        await asyncio.gather(self.run_analysis(), self.run_crawler())
        awe_caller = Caller()

        results = []
        for functionName in constants.AWE_FUNCTIONS:
            functionData = self._lighthouse.get_audit_data(functionName)

            if functionData["failing"] and functionData["applicable"]:
                results.append(
                    awe_caller.run(
                        name=functionName,
                        failingItems=functionData["items"],
                    )
                )

        # Return the flattened result list
        return [result for sublist in results for result in sublist]

    def _reassemble_site(self, function_results):
        """
        Recombines the site's HTML into a more accessible version by replacing
        the offending code with the output of the corresponding AWE function.

        Parameters:
            <list> of accessibility functions results as dictionaries
        """
        site_html = self._crawler.get_html_soup()
        for result in function_results:
            result_soup = result["snippet"]
            # path is in the format "1,HTML,1,BODY,0,DIV,..."
            # we only need to keep the numbers (as integers)
            result_path = [int(i) for i in result["path"].split(",")[::2]]
            self._reassemble_tag(result_soup, result_path, site_html)

    def _reassemble_tag(self, snippet, path, root_html):
        """
        Places a function result into its correct original position

        Parameters:
            snippet <BeautifulSoup> The fixed tag from the accessibility functions
            path <list> The list of integers that path the way to the original tag
            root_html <BeautifulSoup> The HTML of the full site
        Return:
            root_html <BeautifulSoup> The HTML of the full site. Used for recursion

        """
        if len(path) == 0:
            return snippet
        else:
            self._clean_soup_nl(root_html)
            root_html.contents[path[0]] = self._reassemble_tag(snippet, path[1:], root_html.contents[path[0]])
        return root_html

    
    def _clean_soup_nl(self, root_html):
        """
        Removes all children beautiful soup items that only include a new line

        Parameters:
            root_html <BeautifulSoup> The root HTML node
        """
        for child in root_html.children:
            if child == '\n':
                child.extract()
