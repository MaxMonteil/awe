#!/usr/bin/env python

"""
Parses and distributes a Lighthouse audit response to the proper AWE functions.
"""


class ResponseParser:
    """
    The Response Parser class is in charge of parsing the Lighthouse audit
    response into a more manageable format that all AWE functions can refer to.

    Parameters:
        lighthouse_response <str> String response in JSON format
        function_names <list> List of all the supported a11y functions

    Attributes:
        lighthouse_response <str> Where the string response is stored
        auditData <dict> Maps audit data to appropriate AWE function
    """

    def __init__(self, *, lighthouse_response, function_names):
        self._lhResponse = lighthouse_response
        self._functions = function_names
        self._auditData = {}

    def _filter_response_for_accessibility(self):
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
                        "path": node["node"]["path"],
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
            fore = explanation[fore + 1 : fore + 7]
            back = explanation.rfind("#")
            back = explanation[back + 1 : back + 7]

            return {"foreground": fore, "background": back}
        else:
            return {}

    def parse_audit_data(self, force=False):
        """
        Parses the lighthouse response file by calling the cleaning and
        filtering methods on it.

        Only needs to run once but it can be force to run again on the file.

        Parameters:
            force <bool> Default False. If True will parse audit again
        """
        if not self._auditData or force:
            filtered_response, score = self._filter_response_for_accessibility()
            self._auditData = self._clean_response(filtered_response)
            self._auditData["score"] = score

    def get_audit_data(self, functionName=None):
        """
        Getter method to access data related to AWE function.

        Parameters:
            functionName <str> Name of the API function

        Return:
            audit <dict> Function's audit data if functionName is valid
                         If functionName is None returns all parsed data
                         Otherwise returns an empty object
        """
        if functionName in self._auditData:
            return self._auditData[functionName]
        elif functionName is None:
            return self._auditData
        else:
            return {}
