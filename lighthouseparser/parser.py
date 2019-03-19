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

    :param lighthouseResponse: <str> String response in JSON format

    :attr lighthouseResponse: <str> Where the string response is stored
    :attr auditData: <dict> Maps audit data to appropriate AWE function
    '''

    def __init__(self, lighthouseResponse):
        self.lhResponse = json.loads(lighthouseResponse)
        self._auditData = {}

    def filterResponse(self):
        '''
        Removes all unnecessary data from the JSON object.

        :return: <dict> A new dictionary with only the data concerning a11y
        '''

        audits = {
                function: audit for (function, audit) in
                self.lhResponse['audits'].items()
                if function in constants.AWE_FUNCTIONS
                }

        auditRefs = [
                auditRef for auditRef in
                self.lhResponse['categories']['accessibility']['auditRefs']
                if auditRef['id'] in constants.AWE_FUNCTIONS
                ]

        return {
                 'audits': audits,
                 'auditRefs': auditRefs,
                 'score':
                 self.lhResponse['categories']['accessibility']['score']
               }

    def cleanResponse(self, filteredResp):
        '''
        Groups the accessibility data by function.

        :param filteredResp: <JSON> Filtered Lighthouse response
        :return: None
        '''

        for ref in filteredResp['auditRefs']:
            self._auditData[ref['id']] = filteredResp['audits'][ref['id']]
            self._auditData[ref['id']].update(ref)
            self._auditData[ref['id']].pop('id')

    def parseAuditData(self):
        '''
        Driver method to parse audit file.

        :return: <bool> False if data already parsed, True otherwise
        '''
        if self._auditData:
            return False

        self.cleanResponse(self.filterResponse())
        return True

    def getFunctionData(self, functionName):
        '''
        Getter method to access data related to AWE function.

        :param functionName: <str> Name of the API function
        :return: <dict> Function's audit data if valid otherwise an empty dict
        '''

        try:
            return self._auditData[functionName]
        except KeyError:
            return {}
