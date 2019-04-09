from bs4 import BeautifulSoup
from pyppeteer import launch


class Crawler:
    def __init__(self, *, target_url):
        self._target_url = target_url
        self._raw_html = None
        self._bs_html = None

    async def crawl(self):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(self._target_url)
        self._raw_html = await page.content()
        self._bs_html = BeautifulSoup(self._raw_html, "html.parser")
        await browser.close()

    def get_raw_html(self):
        return self._raw_html

    def get_html_soup(self):
        return self._bs_html
