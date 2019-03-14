#!/usr/bin/env python

import os
import json
from constants import AWE_FUNCTIONS
from responseParser import ResponseParser

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
        for funcName in AWE_FUNCTIONS:
            resultFile.write(json.dumps(
                rp.getFunctionData(funcName),
                indent=4,
                sort_keys=True
                ))
