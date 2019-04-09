#!/usr/bin/env python3

"""
Wrapper around the pyppeteer library in charge of crawling a site to get it's HTML and
keep a BeautifulSoup object version.
"""


from bs4 import BeautifulSoup
from io import BytesIO
from pyppeteer import launch


class Crawler:
    """
    Website Crawler for AWE, in charge of scraping the full HTML of the site at the
    given url. It keeps a raw <str> version and a <BeautifulSoup> version for use by
    the engine.

    Parameters:
        target_url <str> URL of the site to crawl

    Attributes:
        _raw_html <str> The raw scraped HTML of the site at target_url
        _bs_html <BeautifulSoup> The parsed HTML of the site
    """
    def __init__(self, *, target_url):
        self._target_url = target_url
        self._raw_html = None
        self._bs_html = None

    async def crawl(self, force=False):
        """
        Goes to the URL class was instantiated with, scrapes the HTML and makes a
        BeautifulSoup version available.

        Parameters:
            force <bool> Whether to force a recrawl or not. Defaults to False.
        """
        if self._raw_html is None or self._bs_html is None or force:
            browser = await launch()
            page = await browser.newPage()
            await page.goto(self._target_url)
            content = await page.content()

            # Raw HTML should be treated as a file in case of transfer
            self._raw_html = BytesIO()
            self._raw_html.write(content.encode())  # Turn <str> into <bytes>
            self._raw_html.seek(0)

            self._bs_html = BeautifulSoup(content, "html.parser")
            await browser.close()

    def get_raw_html(self):
        """Get the raw string format of the scraped HTML."""
        return self._raw_html

    def get_html_soup(self):
        """Get the BeautifulSoup parsed version of the HTML."""
        return self._bs_html
