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
from io import BytesIO
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
        """
        Main Engine entry point.
        Crawls the target site to get it's HTML, runs the Lighthouse Audit on the site,
        and fixes the issues flagged by the audit.

        Returns:
            <BytesIO> the accessible version of the site
        """
        self._reassemble_site(asyncio.run(self._run_functions()))

        # All offending tags will have now been replaced, save to bytes for transfer
        byte_html = BytesIO()
        byte_html.write(self._crawler.get_html_soup().encode())
        byte_html.seek(0)
        return byte_html

    async def _run_functions(self):
        """
        Organizes function calls sending them the proper HTML and Audit data.
        Accessibility functions receive a dictionary with keys:
        ["colors", "selector", "snippet", "path"]

        Keys:
            "color"     foreground and background colors for the color_contrast funct
            "selector"  css selector for the tag.
            "snippet"   failing HTML tag as a string.
            "path"      HTML tree path to the snippet
        """
        await asyncio.gather(self.run_analysis(), self.run_crawler())
        awe_caller = Caller()

        results = []
        for functionName in constants.AWE_FUNCTIONS:
            functionData = self._lighthouse.get_audit_data(functionName)

            if functionData["failing"] and functionData["applicable"]:
                results.append(
                    awe_caller.run(
                        name=functionName, failingItems=functionData["items"]
                    )
                )

        # Return the flattened result list
        return [result for sublist in results for result in sublist]

    def _reassemble_site(self, function_results):
        """
        Recombines the site's HTML into the  accessible version by replacing
        the offending code with the output of the corresponding AWE function.

        Parameters:
            function_results <list> Collection of the function result objects
        """
        for result in function_results:
            # path is in the format "1,HTML,1,BODY,0,DIV,..."
            # we only need to keep the numbers (as integers)
            path_indices = [int(i) for i in result["path"].split(",")[::2]]
            self._find_and_replace_tag(
                html=self._crawler.get_html_soup(),
                full_path=path_indices,
                snippet=result["snippet"],
            )

    def _find_and_replace_tag(self, html, full_path, snippet):
        """
        Tail recursive method that searches for the original snippet at 'full_path' and
        replaces it with the fixed 'snippet'.

        Parameters:
            html <BeautifulSoup> The HTML of the full site
            full_path <list> The list of integers that path the way to the original tag
            snippet <BeautifulSoup> The fixed tag from the accessibility functions
        """
        # We add 1 to account for the behavior of contents but the first index which
        # points to HTML is correct and always 1, so subtracting one makes it 0
        full_path[0] = 0

        def tag_finder(curr, path):
            if path:
                return tag_finder(
                    # .contents also has newlines as children, this messes up indices
                    curr=curr.contents[path[0] + 1],  # +1 to account for '\n'
                    path=path[1:],
                )
            return curr

        tag_finder(html, full_path).replace_with(snippet)
