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
        target_url <str> URL of the target website
        audit_format <str> Format in which lighthouse should return the audit

    Properties:
       audit <str> JSON of parsed lighthouse audit
       site_html <BytesIO> Scraped HTML as a BytesIO object for transfers
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

    @property
    def audit(self):
        """Get the full parsed audit"""
        if self._audit_format == "json":
            return self._lighthouse.audit
        else:
            return self._lighthouse.lighthouse_audit

    async def run_crawler(self, force=False):
        """
        Crawls the site and scrapes the HTML.

        Parameters:
            force <bool> Force a rerun of the crawl
        """
        await self._crawler.crawl(force)

    @property
    def site_html(self):
        """Get the scraped HTML as a BytesIO file-like format for transfers."""
        return self._crawler.raw_html

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
        byte_html.write(self._crawler.html_soup.encode())
        byte_html.seek(0)
        return byte_html

    async def _run_functions(self):
        """
        Organizes function calls sending them the proper HTML and Audit data.
        Accessibility functions receive a dictionary with keys:
        ["colors", "selector", "snippet", "path"]

        Function data keys:
            "color"     foreground and background colors for the color_contrast funct
            "selector"  css selector for the tag.
            "snippet"   failing HTML tag as a string.
            "path"      HTML tree path to the snippet
        """
        await asyncio.gather(self.run_analysis(), self.run_crawler())

        # results = []
        # for name, data in self._lighthouse:
        #     if data["failing"] and data["applcable"]:
        #         results.extend(Caller.run(name=name, failingItems=data))

        return (
            result
            for name, data in self._lighthouse
            for result in Caller.run(name=name, failingItems=data)
            if data["failing"] and data["applicable"]
        )

    def _reassemble_site(self, function_results):
        """
        Recombines the site's HTML into a more accessible version by replacing
        the offending code with the output of the corresponding AWE function.

        Parameters:
            function_results <list> Collection of the function result objects
        """
        for result in function_results:
            # path is in the format "1,HTML,1,BODY,0,DIV,..."
            # we only need to keep the numbers (as integers)
            snippet_path = [int(i) for i in result["path"].split(",")[::2]]
            # self._find_and_replace_tag(result["snippet"], snippet_path)
            self._reassemble_tag(
                result["snippet"], snippet_path, self._crawler.html_soup
            )

    # Another implemntation of the reassembler (see call on line 135)
    # def _find_and_replace_tag(self, snippet, snippet_path):
    #     curr_tag = self._crawler.html_soup
    #     for i in snippet_path:
    #         # get tag contents(children), filter out white-space, reassign from index
    #         curr_tag = [tag for tag in curr_tag.contents if not str(tag).isspace()][i]

    #     curr_tag.replace_with(snippet)

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
            root_html.contents[path[0]] = self._reassemble_tag(
                snippet, path[1:], root_html.contents[path[0]]
            )
        return root_html

    def _clean_soup_nl(self, root_html):
        """
        Removes all children beautiful soup items that only include a new line

        Parameters:
            root_html <BeautifulSoup> The root HTML node
        """
        for child in root_html.children:
            if child == "\n":
                child.extract()
