#!/usr/bin/env python

'''
Parses and distributes a Lighthouse audit response to the proper AWE functions.
'''

import constants
import json


class ResponseParser:
    '''
    The Response Parser class is in charge of parsing the Lighthouse audit
    response into a more manageable format that all AWE functions can refer to.

    Parameters:
        lighthouseResponse <str> String response in JSON format

    Attributes:
        lighthouseResponse <str> Where the string response is stored
        auditData <dict> Maps audit data to appropriate AWE function
    '''

    def __init__(self, lighthouseResponse):
        self._lhResponse = json.loads(lighthouseResponse)
        self._auditData = {}

    def _filter_response(self):
        '''
        Removes all data from lighthouse response that isn't about
        accessibility or about one of the AWE functions.

        Return:
            <dict> AWE function names mapped to lighthouse audit data
        '''
        # Keep all dict values relating to AWE functions and set the function
        # name as the key
        filtered = {
            function: audit for (function, audit) in
            self._lhResponse['audits'].items()
            if function in constants.AWE_FUNCTIONS
        }

        filtered['score'] = (self._lhResponse['categories']
                                             ['accessibility']
                                             ['score'])

        return filtered

    def _clean_response(self, filteredResp):
        '''
        Groups the accessibility data by function.

        Parameters:
            filteredResp <JSON> Filtered Lighthouse response
        '''
        for ref in filteredResp['auditRefs']:
            self._auditData[ref['id']] = filteredResp['audits'][ref['id']]
            self._auditData[ref['id']].update(ref)
            self._auditData[ref['id']].pop('id')

    def parse_audit_data(self):
        '''
        Driver method to parse audit file.

        Return:
            <bool> False if data already parsed, True otherwise
        '''
        if self._auditData:
            return False

        self._clean_response(self._filter_response())
        return True

    def get_function_data(self, functionName):
        '''
        Getter method to access data related to AWE function.

        Parameters:
            functionName <str> Name of the API function

        Return:
            <dict> Function's audit data if valid otherwise an empty dict
        '''
        try:
            return self._auditData[functionName]
        except KeyError:
            return {}
