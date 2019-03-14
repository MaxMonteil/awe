#!/usr/bin/env python

'''
Parses and distributes a Lighthouse audit response to the proper AWE functions.
'''

import json
from constants import AWE_FUNCTIONS


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
        self.auditData = {}

    def filterResponse(self):
        '''
        Removes all unnecessary data from the JSON object.

        :return: <dict> A new dictionary with only the data concerning a11y
        '''

        audits = {
                function: audit for (function, audit) in
                self.lhResponse['audits'].items()
                if function in AWE_FUNCTIONS
                }

        auditRefs = [
                auditRef for auditRef in
                self.lhResponse['categories']['accessibility']['auditRefs']
                if auditRef['id'] in AWE_FUNCTIONS
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
        :return: <JSON> Lighthouse response organized by AWE function
        '''

        clean = {}

        for ref in filteredResp['auditRefs']:
            clean[ref['id']] = filteredResp['audits'][ref['id']]
            clean[ref['id']].update(ref)
            clean[ref['id']].pop('id')

        return clean


if __name__ == '__main__':
    print(AWE_FUNCTIONS)
