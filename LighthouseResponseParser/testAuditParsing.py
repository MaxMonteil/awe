#!/usr/bin/env python

import os
from constants import AWE_FUNCTIONS
from responseParser import ResponseParser

LIGHTHOUSE_AUDIT_PATH = '../testData/lighthouseResponse.json'


def test(auditFilePath):
    rp = ResponseParser(readAuditFile(auditFilePath))
    rp.parseAuditData()

    return rp.getFunctionData(AWE_FUNCTIONS[0])


def readAuditFile(filePath):
    audit = ''

    with open(filePath, 'r') as auditFile:
        audit = auditFile.read()

    return audit


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    result = test(os.path.join(dirname, LIGHTHOUSE_AUDIT_PATH))

    print(result)
