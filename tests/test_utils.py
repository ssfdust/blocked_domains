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
    tests.test_utils
    ~~~~~~~~~~~~~~~~~~
    测试组件模块
"""
import pytest

from blocked_domain_generator.utils import trim_dot, combine_set, difference_set


@pytest.mark.parametrize(
    "text, result", [("..1212", ".1212"), (".abc.com", "abc.com"), ("test", "test")]
)
def test_trim_dot(text, result):
    assert trim_dot(text) == result


@pytest.mark.parametrize(
    "args, result",
    [
        ([{1, 2, 3, 4}, {4, 6, 7}, {9, -1}], {-1, 1, 2, 3, 4, 6, 7, 9}),
        ([{1, 3}, {2, 4}], {1, 2, 3, 4}),
    ],
)
def test_combine_set(args, result):
    assert combine_set(*args) == result


@pytest.mark.parametrize(
    "parent, child, result", [({1, 2, 3, 4}, {4, 2}, {1, 3}), ({1, 3}, {3, 4}, {1})]
)
def test_difference_set(parent, child, result):
    assert difference_set(parent, child) == result
