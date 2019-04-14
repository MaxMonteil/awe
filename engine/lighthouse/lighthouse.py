#!/usr/bin/env python3

from .parser import ResponseParser
from io import BytesIO
import asyncio
import json

# import subprocess

"""
Wrapper class for Google Lighthouse and the response parsing module.
"""


class Lighthouse:
    """
    This is a higher level class meant as a wrapper for Google Lighthouse and its
    response parser.

    Parameters:
        function_names <list> List of all the supported a11y functions
        target_url <str> URL of the target website
        audit_format <str> Format in which lighthouse should return the audit


    Properties:
        audit <str> Parsed JSON response mapping data to appropriate AWE function
        score <int> Score given to the site by Lighthouse
        lighthouse_audit <BytesIO> File like object with full lighthouse audit
    """

    def __init__(self, *, function_names, target_url, audit_format="json"):
        self._function_names = function_names
        self._target_url = target_url
        self._audit_format = audit_format
        self._lighthouse_response = None
        self._parser = None

    async def run(self, force=False):
        """Run lighthouse on the target site and parse the JSON response."""
        self._lighthouse_response = await self._run_lighthouse_audit()
        if self._audit_format == "json":
            self._run_parser(force)

    # Non async version just in case
    # def _run_lighthouse_audit(self):
    #     completed_process = subprocess.run(
    #        [
    #            "bash",
    #            "./engine/lighthouse/run_lighthouse.sh",
    #            self._target_url,
    #            self._audit_format,
    #        ],
    #        capture_output=True,  # Avoid creating a file, keep it in memory
    #     )

    #     if self._audit_format == "json":
    #         return json.loads(completed_process.stdout)
    #     else:
    #         # save the bytestring output as a file-like object for transfers
    #         s = BytesIO()
    #         s.write(completed_process.stdout)
    #         s.seek(0)
    #         return s

    async def _run_lighthouse_audit(self):
        """Run lighthouse audit on the target site."""
        command = f"""bash ./engine/lighthouse/run_lighthouse.sh \
        {self._target_url} {self._audit_format}"""

        proc = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if stderr:
            error_msg = f"Lighthouse exited with {proc.returncode}\n{stderr.decode()}"
            raise SystemError(error_msg)

        # stdout is a byte string
        return stdout

    def _run_parser(self, force):
        if self._parser is None:
            self._parser = ResponseParser(
                lighthouse_response=json.loads(self._lighthouse_response),
                function_names=self._function_names,
            )
        self._parser.parse_audit_data(force)

    @property
    def audit(self):
        """Parsed JSON lighthouse audit."""
        return json.dumps(self._parser.audit)

    @property
    def score(self):
        """Lighthouse audit score of the site."""
        return self._parser.score

    @property
    def lighthouse_audit(self):
        """Returns lighthouse audit as a file-like object for transfers."""
        f = BytesIO()
        f.write(self._lighthouse_response)
        f.seek(0)
        return f

    def __len__(self):
        return len(self._parser)

    def __getitem__(self, key):
        if key not in self._parser:
            raise KeyError

        return self._parser[key]

    def __iter__(self):
        return iter(self._parse)
