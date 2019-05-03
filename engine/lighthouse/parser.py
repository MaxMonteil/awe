#!/usr/bin/env python3

"""
Parses a JSON Lighthouse audit response keeping information relating to accessibility
and organizing it according to AWE functions. It also offers the a list of failing tags
with their function pipeline.
"""

from collections import namedtuple


class ResponseParser:
    """
    The Response Parser class is in charge of parsing the Lighthouse audit
    response into a more manageable format that all AWE functions can refer to.

    Parameters:
        lighthouse_response <str> String response in JSON format
        function_names <namedtuple> Tuple of all the supported a11y functions
            fields:
                INDIRECT <tuple> A11y functions that accept and fix a snippet
                DIRECT <tuple> A11y functions that change the original HMTL directly

    Properties:
        audit <dict> Parsed response mapping data to appropriate AWE function
        failed_audits <list> Tags with a list of their failing functions sorted by path
        score <int> Score given to the site by Lighthouse
    """

    def __init__(self, *, lighthouse_response, function_names):
        self._lh_response = lighthouse_response
        self._functions = function_names
        self._audit_data = None
        self._lh_score = None
        self._parsed_tags = namedtuple("parsed_tags", ["indirect", "direct"])

    def parse_audit_data(self, force=False):
        """
        Parses the full lightouse response keeping only accessibility related
        information and additional values needed by the Engine.

        Only needs to run once but it can be forced to run again on the audit.

        Parameters:
            force <bool> Default False. If True will parse lighthouse audit again.
        """
        if not self._audit_data or force:
            self._lh_score = self._lh_response["categories"]["accessibility"]["score"]
            self._audit_data = dict(
                self._parse_lighthouse_response(self._lh_response, self._functions.ALL)
            )

    @property
    def audit(self):
        return self._audit_data

    @property
    def failed_audits(self):
        """Collection of the audits that failed lighthouse tests."""
        try:
            return self._parsed_tags(
                indirect=self._pipeline_function_data(
                    (
                        item
                        for data in self._audit_data.values()
                        for item in data["items"]
                    ),
                    self._functions.INDIRECT,
                ),
                direct=self._pipeline_function_data(
                    (
                        item
                        for data in self._audit_data.values()
                        for item in data["items"]
                    ),
                    self._functions.DIRECT,
                ),
            )
        except AttributeError:
            return None

    @property
    def score(self):
        return self._lh_score

    def _parse_lighthouse_response(self, lighthouse_response, functions):
        """
        Keeps only accessibility related audit data as well as information about the
        tags such as failing/applicable, and the description.

        Yield:
            <tuple>(<str>, <dict>)
                Pair of function name and data
                data:
                    "failing"       <bool> Whether the tag is failing the a11y test
                    "applicable"    <bool> Whether the a11y test is actually applicable
                    "description"   <str> Lighthouse description of the function role
                    "items"         <generator> Cleaned list of item dict
        """
        # Keep all dict values relating to AWE functions and set the function
        # name as the key
        for function_name, audit in lighthouse_response["audits"].items():
            if function_name in functions:
                yield (
                    function_name,
                    {
                        # failing: the function was tested and it did not pass WCAG
                        "failing": False if audit["score"] == 1 else True,
                        # applicable: the function can't be tested
                        "applicable": audit["score"] is not None,
                        "description": audit["description"],
                        "items": list(
                            self._parse_audit_items(
                                audit.get("details", {}).get("items", []), function_name
                            )
                        ),
                    },
                )

    def _parse_audit_items(self, items, function_name):
        """
        Parses the list of the function's information for the function into the format
        needed by the Engine and the accessibility functions.

        Parameters:
            items <list> the Lighthouse information associated with the function
            function_name <str> Name of the function whos data is being parsed

        Yield:
            <dict> Mapping of useful values from the filtered response
        """
        for item in items:
            if item["node"]["path"]:
                yield {
                    "snippet": item["node"]["snippet"],
                    "selector": item["node"]["selector"],
                    "colors": self._extract_hex_codes(item["node"]["explanation"]),
                    "pipeline": [function_name],
                    # path is in the format "1,HTML,1,BODY,0,DIV,..."
                    # we only need to keep the numbers (as integers)
                    "path": tuple(int(i) for i in item["node"]["path"].split(",")[::2]),
                }

    def _pipeline_function_data(self, function_data_seq, function_list):
        """
        Reduces the function data into a list of objects with the pipeline of the
        accessibility functions the tag needs to go through. It is sorted by path
        length in order to replace parent tags before children tags.

        Parameters:
            function_data_seq <generator> Sequence of function's audit data

        Return:
            <list> list of function data unique by tags, sorted by path length
        """
        result = {}
        for data in function_data_seq:
            if data["pipeline"][0] in function_list:
                try:
                    result[data["path"]]["pipeline"].extend(data["pipeline"])
                except KeyError:
                    result[data["path"]] = data
                finally:
                    # keep the "colors" value of the snippets that fail color-contrast
                    if data["pipeline"][0] == "color-contrast":
                        result[data["path"]]["colors"] = data["colors"]

        return sorted(result.values(), key=lambda value: len(value["path"]))

    def _extract_hex_codes(self, explanation):
        """
        Extract the two hexadecimal codes in the explanation which represent the
        foreground and the background colors.

        Parameters:
            explanation <str> Explanation of what is wrong and how to fix it

        Return:
            colors <dict> Hex foreground and background colors if it is the
                          color-contrast explanation, empty object otherwise
        """
        fore = explanation.find("#")
        # Hash was not found means that this wasn't the 'color-contrast' function
        if fore != -1:
            fore = explanation[fore + 1 : fore + 7]
            back = explanation.rfind("#")
            back = explanation[back + 1 : back + 7]

            return {"foreground": fore, "background": back}
        else:
            return {}

    def __len__(self):
        return len(self._audit_data)

    def __getitem__(self, function_name):
        if function_name not in self._audit_data:
            raise KeyError

        return self._audit_data[function_name]

    def __contains__(self, key):
        return key in self._audit_data

    def __iter__(self):
        return iter(self._audit_data.items())
