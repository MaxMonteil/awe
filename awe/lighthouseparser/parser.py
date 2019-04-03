#!/usr/bin/env python

"""
Parses and distributes a Lighthouse audit response to the proper AWE functions.
"""

import json


class ResponseParser:
    """
    The Response Parser class is in charge of parsing the Lighthouse audit
    response into a more manageable format that all AWE functions can refer to.

    Parameters:
        lighthouseResponse <str> String response in JSON format
        functionNames <list> List of all the supported a11y functions

    Attributes:
        lighthouseResponse <str> Where the string response is stored
        auditData <dict> Maps audit data to appropriate AWE function
    """

    def __init__(self, *, lighthouseResponse, functionNames):
        self._lhResponse = json.loads(lighthouseResponse)
        self._functions = functionNames
        self._auditData = {}

    def _filter_response(self):
        """
        Removes all data from lighthouse response that isn't about
        accessibility or about one of the AWE functions.

        Return:
            <dict> AWE function names mapped to lighthouse audit data
        """
        # Keep all dict values relating to AWE functions and set the function
        # name as the key
        filtered = {
            function: audit for (function, audit) in
            self._lhResponse["audits"].items()
            if function in self._functions
        }

        filtered["score"] = self._lhResponse["categories"]["accessibility"]["score"]

        return filtered

    def _clean_response(self, filtered):
        """
        Cleans the filtered response from any unnecessary values.

        Parameters:
            filtered <JSON> Filtered Lighthouse response
        """
        return {
            functionName: {
                "failing": False if data["score"] == 1 else True,
                "items": [node["snippet"] for node in data["details"]["items"]]
            }
            for (functionName, data) in filtered.items()
        }

    def parse_audit_data(self, force=False):
        """
        Parses the lighthouse response file by calling the cleaning and
        filtering methods on it.

        Only needs to run once but it can be force to run again on the file.

        Parameters:
            force <bool> Default False. If True will parse audit again
        """
        if not self._auditData or force:
            self._auditData = self._clean_response(self._filter_response())

    def get_audit_data(self, functionName=None):
        """
        Getter method to access data related to AWE function.

        Parameters:
            functionName <str> Name of the API function

        Return:
            <dict> Function's audit data if valid otherwise an empty dict
                   If functionName is None returns all parsed data
        """
        try:
            if functionName:
                return self._auditData[functionName]

            return self._auditData
        except KeyError:
            return {}
