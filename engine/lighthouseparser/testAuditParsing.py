#!/usr/bin/env python

from parser import ResponseParser
import constants
import json
import os

LIGHTHOUSE_AUDIT_PATH = '../testData/lighthouseResponse.json'


def test(auditFilePath):
    rp = ResponseParser(readAuditFile(auditFilePath))
    rp.parseAuditData()

    return rp


def readAuditFile(filePath):
    audit = ''

    with open(filePath, 'r') as auditFile:
        audit = auditFile.read()

    return audit


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, LIGHTHOUSE_AUDIT_PATH)

    rp = test(filepath)

    with open('testResults.json', 'w+') as resultFile:
        for funcName in constants.AWE_FUNCTIONS:
            resultFile.write(json.dumps(
                rp.getFunctionData(funcName),
                indent=4,
                sort_keys=True
                ))
