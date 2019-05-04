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
from .functions import caller as Caller
from .lighthouse import Lighthouse
from collections import namedtuple
from io import BytesIO
import asyncio
from bs4 import BeautifulSoup, element


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

        self._accessible_site = None

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

    async def run_engine(self):
        """
        Main Engine entry point.
        Crawls the target site to get it's HTML, runs the Lighthouse Audit on the site.

        Sends each tag through it's pipeline.
        Accessibility functions receive a dictionary with keys:
        ["colors", "selector", "snippet", "path"]

        Function data keys:
            "color"     foreground and background colors for the color_contrast funct
            "selector"  css selector for the tag
            "snippet"   failing HTML tag as a string
            "path"      HTML tree path to the snippet
            "pipeline"  List of the functions the snippet needs to go through

        Returns:
            <BytesIO> the accessible version of the site
        """
        await asyncio.gather(self.run_analysis(), self.run_crawler())

        # Cylinder 1: Indirect functions
        fixed_tags = (
            Caller.run_pipeline(tag) for tag in self._lighthouse.failed_audits.indirect
        )
        self._reassemble_site(fixed_tags)

        # Cylinder 2: Direct functions
        html_and_tag = namedtuple("html_and_tag", ["html", "tag_data"])
        for tag in self._lighthouse.failed_audits.direct:
            Caller.run_pipeline(html_and_tag(html=self._crawler.html_soup, tag_data=tag))

        # All failing snippets will have now been replaced, save to bytes for transfer
        byte_html = BytesIO()
        byte_html.write(self._crawler.html_soup.encode())
        byte_html.seek(0)
        self._accessible_site = byte_html

    @property
    def accessible_site(self):
        return self._accessible_site

    def _reassemble_site(self, fixed_tags):
        """
        Recombines the site's HTML into a more accessible version by replacing
        the offending code with the output of the corresponding AWE function.

        Parameters:
            function_results <list> Collection of the function result objects
        """
        for tag in fixed_tags:
            self._find_and_replace_snippet(tag["snippet"], tag["path"])

    def _find_and_replace_snippet(self, snippet, path):
        """
        Navigates the HTML tree down to the tag and replaces it with the fixed snippet.
        """
        curr_tag = self._crawler.html_soup
        try:
            for i in path:
                # get tag contents(children), filter out white-space, reassign from index
                curr_tag = [tag for tag in curr_tag.contents if not str(tag).isspace()][i]

            if snippet.isSelfClosing or snippet.is_empty_element:
                curr_tag.replace_with(snippet)
            else:
                for child in curr_tag.children:
                    if not str(child).isspace():
                        tag = str(child.extract())
                        if type(child) is element.Tag:
                            snippet.append(BeautifulSoup(tag, "html.parser").find())
                        elif type(child) is element.NavigableString:
                            snippet.string.replace_with(tag)

                curr_tag.replace_with(snippet)
        except IndexError:
            # The crawler obtained a different site HTML than what Lighthouse did
            # causing a mismatch and thus an unreachable file
            pass
