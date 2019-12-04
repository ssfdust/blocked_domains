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
    blocked_domain_generator.crawlers.file
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    文件爬取器
"""

import httpx

from blocked_domain_generator.crawlers.base import Crawler, RequestState
from blocked_domain_generator.parsers.ads import BanListParser, FileParser, HostParser


class BaseFileCrawler(Crawler):
    def _handle_ok(self, response: httpx.Response) -> int:
        self.data = response.content.decode("utf-8")
        return RequestState.Ok


class FileCrawler(BaseFileCrawler, FileParser):
    pass


class BanListCrawler(BaseFileCrawler, BanListParser):
    pass


class HostCrawler(BaseFileCrawler, HostParser):
    pass
