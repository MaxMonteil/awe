#!/usr/bin/env python

from parser import ResponseParser
from pathlib import Path
import constants
import json
import sys


def test(auditFilePath, names):
    with open(auditFilePath, "r") as auditFile:
        rp = ResponseParser(
            lighthouseResponse=auditFile.read(),
            functionNames=names
        )
        rp.parse_audit_data()

        return rp


if __name__ == "__main__":
    AUDIT_FILE = Path.cwd().joinpath("engine/lighthouseparser/audit.json")

    OUTPUT_FILE = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    OUTPUT_FILE = OUTPUT_FILE.joinpath("results/testResult.json")

    rp = test(AUDIT_FILE, constants.AWE_FUNCTIONS)

    with open(OUTPUT_FILE, "w+") as resultFile:
        resultFile.write(json.dumps(
                rp.get_audit_data(),
                indent=4,
                sort_keys=True,
            )
        )
