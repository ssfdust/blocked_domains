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
    blocked_domain_generator.utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    工具组件模块
"""
from pathlib import Path
from typing import Set, List
import re

DIST = "sites"

schema_regex = re.compile(r"http[s]{0,1}://")


def trim_dot(text: str) -> str:
    if text.startswith("."):
        return text[1:]
    return text


def combine_set(*args: Set) -> Set:
    """多个集合的交集"""
    result = set()
    for ele in args:
        result = result | ele

    return result


def difference_set(parent: Set, child: Set) -> Set:
    """求父集的补集"""
    return parent ^ child & parent


def chunks(lst: List, chunk_size: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def drop_schema(url: str) -> str:
    return re.sub(schema_regex, "", url)


def get_dist_path(create=True) -> Path:
    dist_path = Path().joinpath(DIST)
    if not dist_path.exists() and create:
        dist_path.mkdir()
    return dist_path


def dump_to_dist(records: Set, filename: str):
    dist_path = get_dist_path()
    filepath = dist_path.joinpath(filename)

    last = records.pop()

    with filepath.open("a") as buf:
        for record in records:
            buf.write(record + "\n")
        buf.write(last)
