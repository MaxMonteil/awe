#!/usr/bin/env python3

"""
Parses a JSON Lighthouse audit response keeping information relating to accessibility
and organizing it according to AWE functions.
"""


class ResponseParser:
    """
    The Response Parser class is in charge of parsing the Lighthouse audit
    response into a more manageable format that all AWE functions can refer to.

    Parameters:
        lighthouse_response <str> String response in JSON format
        function_names <list> List of all the supported a11y functions

    Properties:
        audit <dict> Parsed response mapping data to appropriate AWE function
        score <int> Score given to the site by Lighthouse
    """

    def __init__(self, *, lighthouse_response, function_names):
        self._lhResponse = lighthouse_response
        self._functions = function_names
        self._audit_data = None
        self._audit_score = None

    def parse_audit_data(self, force=False):
        """
        Parses the lighthouse response file by calling the cleaning and
        filtering methods on it.

        Only needs to run once but it can be force to run again on the file.

        Parameters:
            force <bool> Default False. If True will parse audit again
        """
        if not self._audit_data or force:
            filtered_response, self._audit_score = self._filter_for_accessibility()
            self._audit_data = self._clean_response(filtered_response)

    def _filter_for_accessibility(self):
        """
        Removes all data from lighthouse response that isn't about
        accessibility or about one of the AWE functions.

        Return:
            <dict> AWE function names mapped to lighthouse audit data
        """
        # When a function is not applicable (eg: audio-caption on a page with no audio
        # content) the node does not have a "details" key. This placeholder serves to
        # give the node a default value while looping through them
        placeholder = {"details": {"items": []}}

        # Keep all dict values relating to AWE functions and set the function
        # name as the key
        filtered = {
            function: dict(placeholder, **audit)
            for (function, audit) in self._lhResponse["audits"].items()
            if function in self._functions
        }

        score = self._lhResponse["categories"]["accessibility"]["score"]

        return filtered, score

    def _clean_response(self, filtered):
        """
        Cleans the filtered response from any unnecessary values.

        Parameters:
            filtered <JSON> Filtered Lighthouse response

        Return:
            cleaned <dict> Mapping of useful values from the filtered response
        """
        # failing: the function was tested and it did not pass WCAG
        # applicable: unknown if it passed or failed, the function can't be tested
        return {
            functionName: {
                "failing": False if data["score"] == 1 else True,
                "applicable": data["score"] is not None,
                "description": data["description"],
                "items": [
                    {
                        "snippet": node["node"]["snippet"],
                        "selector": node["node"]["selector"],
                        "colors": self._extract_hex_codes(node["node"]["explanation"]),
                        # path is in the format "1,HTML,1,BODY,0,DIV,..."
                        # we only need to keep the numbers (as integers)
                        "path": [int(i) for i in node["node"]["path"].split(",")[::2]],
                    }
                    for node in data["details"]["items"]
                ],
            }
            for (functionName, data) in filtered.items()
        }

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
            fore = explanation[fore + 1: fore + 7]
            back = explanation.rfind("#")
            back = explanation[back + 1: back + 7]

            return {"foreground": fore, "background": back}
        else:
            return {}

    @property
    def audit(self):
        return self._audit_data

    @property
    def score(self):
        return self._audit_score

    def __len__(self):
        return len(self._audit_data)

    def __getitem__(self, function_name):
        if function_name not in self._audit_data:
            raise KeyError

        return self._audit_data[function_name]

    def __iter__(self):
        return iter(self._audit_data.items())
