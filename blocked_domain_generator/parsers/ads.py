#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
    blocked_domain_generator.parsers.adparser
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    广告列表处理
"""

from blocked_domain_generator.parsers.base import BaseParser
from blocked_domain_generator.utils import trim_dot

DOMAIN_POSTION = 1


class FileParser(BaseParser):
    def parse(self):
        record = set()

        for line in self.data.split("\n"):
            result = self._parse_line(line)
            if result:
                record.add(trim_dot(result))

        self.extract = record

    @staticmethod
    def _parse_line(line: str) -> str:
        #  if "Reject" in line and "DOMAIN-SUFFIX" in line:
        #      return trim_dot(line.split(',')[DOMAIN_POSTION])
        return line


class BanListParser(FileParser):
    @staticmethod
    def _parse_line(line: str) -> str:
        if "Reject" in line and "DOMAIN-SUFFIX" in line:
            return line.split(",")[DOMAIN_POSTION]
        return ""


class HostParser(FileParser):
    @staticmethod
    def _parse_line(line: str) -> str:
        if "0.0.0.0" in line:
            return line.split()[DOMAIN_POSTION]
        return ""
