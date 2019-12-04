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
    tests.cralers.test_crawler
    ~~~~~~~~~~~~~~~~~~~
    测试是否爬取到网站内容
"""
import pytest
import respx

from blocked_domain_generator.crawlers.base import Crawler, ConnectTimeout
from blocked_domain_generator import const


@pytest.mark.trio
async def test_website_loaded():
    crawler = Crawler(const.PORNDUDE)

    await crawler.load_website()

    assert crawler.data is not None and "Porn Dude" in crawler.data


@pytest.mark.trio
@respx.mock
async def test_client_with_exceptions():
    respx.get("http://test_exceptions", content=ConnectTimeout())
    crawler = Crawler("http://test_exceptions")

    with pytest.raises(Exception):
        await crawler.load_website()


@pytest.mark.trio
@respx.mock
@pytest.mark.parametrize("code, headers", [(429, {"retry-after": "3000"}), (500, {})])
async def test_resp_error(code, headers):
    respx.get("http://test_resp_error", status_code=code, headers=headers)
    crawler = Crawler("http://test_resp_error")

    with pytest.raises(RuntimeError):
        await crawler.load_website()
