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
    tests.parsers.test_cate
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    测试分类器
"""
import pytest
from blocked_domain_generator.parsers.cate import (
    title_regex,
    re,
    wildchar_regex,
    num_regex,
)


@pytest.mark.parametrize(
    "title",
    [
        "123色情123",
        "123情色123",
        "111成人123",
        "11性爱111",
        "1122女优1111情色",
        "三陪123",
        "1212艳照门情色",
    ],
)
def test_regex(title):
    matched = re.match(title_regex, title)

    assert matched


@pytest.mark.parametrize(
    "url, result",
    [
        ("www.baidu.com", False),
        ("https://www.baidu.com/abc", True),
        ("http:www//baidu.com/aa", False),
        ("http://www.baidu.com", True),
    ],
)
def test_wildchar_match(url, result):
    matched = re.match(wildchar_regex, url) is not None
    assert matched is result


@pytest.mark.parametrize(
    "text, result",
    [("www.123.com", 123), ("www.098", 98), ("008977www.baidu.com", 8977),],
)
def test_num_match(text, result):
    matched = re.match(num_regex, text)
    assert int(matched.group(1)) == result
