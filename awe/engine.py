#!/usr/bin/env python

"""
Main class for the Accessibility Web Engine.

Holds the true copies of the target page HTML as well as the parsed Lighthouse
Audit results. AWE then segments and distributes these files to the concerned accessibility functions.

Finally, it reassembles the function outputs into the accessible version of the
target site.
"""

# TODO
# from crawler.crawler import HTMLCrawler
# from lighthouse import lighthouseAuditer

from functions import Caller as AWECaller
from lighthouseparser import ResponseParser
import constants


class Engine:
    """"""
    def __init__(self, target_url):
        # Get the Lighthouse audit
        # audit_data = lighthouseAuditer(target_url)
        audit_data = "{}"  # placeholder

        # Parse result of audit
        lhAudit = ResponseParser(
            lighthouseResponse=audit_data,
            functionNames=constants.AWE_FUNCTIONS,
        )

        lhAudit.parse_audit_data()

        # Get HTML of the target site, would be a bs4 object
        # target_HTML = HTMLCrawler(TARGET_URL)

        self.run_engine(lhAudit)

    def run_engine(self, lhAudit):
        """
        Organizes function calls sending them the proper HTML and Audit data.

        Parameters:
            lhAudit <ResponseParser> Parser object with the parsed Lighthouse audit
        """
        awe_caller = AWECaller()

        result = {}

        for functionName in constants.AWE_FUNCTIONS:
            functionData = lhAudit.get_function_data(functionName)

            if functionData["failing"]:
                result[functionName] = awe_caller.run(
                    name=functionName,
                    failingItems=functionData["items"],
                )

        return result

    def reassemble_site(self):
        """
        Recombines the site's HTML into a more accessible version by replacing
        the offending code with the output of the corresponding AWE function.
        """
        pass
