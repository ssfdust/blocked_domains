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
    tests.crawlers.test_file
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    测试文件爬虫
"""
import pytest

from blocked_domain_generator.crawlers.file import BaseFileCrawler
from blocked_domain_generator.const import BlockListFiles as filelst


@pytest.mark.trio
@pytest.mark.parametrize(
    "url", [filelst.banlist, filelst.hosts, filelst.v2ray, filelst.ad_blank]
)
async def test_file_crawler(url):
    crawler = BaseFileCrawler(url)
    await crawler.load_website()
    assert isinstance(crawler.data, str)
