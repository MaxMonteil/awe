#!/usr/bin/env python

from parser import ResponseParser
import json
import subprocess


class Lighthouse:
    def __init__(self, *, function_names, target_url, audit_format="json"):
        self._function_names = function_names
        self._target_url = target_url
        self._audit_format = audit_format
        self._lighthouse_response = None
        self._parser = None

    def run(self, force=False):
        self._run_lighthouse_audit()
        self._build_parser()
        self._run_parser(force)

    def _run_lighthouse_audit(self):
        completed_process = subprocess.run(
            [
                "bash",
                "./engine/lighthouse/run_lighthouse.sh",
                self._target_url,
                self._audit_format,
            ],
            capture_output=True  # Avoid creating a file, keep it in memory
        )

        self._lighthouse_response = json.loads(completed_process.stdout)

    def _build_parser(self):
        self._parser = ResponseParser(
            lighthouse_response=self._lighthouse_response,
            function_names=self._function_names
        )

    def get_audit_data(self, function_name=None):
        return self._parser.get_audit_data(function_name)

    def _run_parser(self, force=False):
        if self._parser is None:
            self._parser = self._lighthouse_response

        self._parser.parse_audit_data(force)
