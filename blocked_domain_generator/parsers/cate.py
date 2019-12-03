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
    blocked_domain_generator.parsers.cate
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    提取所有的文字类别，且归类
"""
import re
import logging
from typing import List, Dict, Union

from bs4 import Tag

from blocked_domain_generator import const

from .base import BaseParser

logging.basicConfig(level=logging.INFO)

title_regex = re.compile(r".*({}).*".format("|".join(const.KEY_WORD)))

wildchar_regex = re.compile(r"^http[s]{0,1}://.*")

num_regex = re.compile(r"[^\d]*(\d+)[^\d]*")


class CateParser(BaseParser):
    def parse(self) -> List[Tag]:
        if self.bs4 is None:
            self.init_parser()

        blocks = self._parse_div_block()
        self.extract = self._filter_and_extract(blocks)

        return self.extract

    def _parse_div_block(self) -> List[Tag]:
        blocks = list(
            tag for tag in self.bs4.find_all(const.DIV_TAG, class_=const.CATE_CLASS)
        )

        return blocks

    def _filter_and_extract(self, div_blocks: List[Tag]) -> Dict[str, Tag]:
        filtered_blocks = {}

        for block in div_blocks:
            title = block.h2.text
            if re.match(title_regex, title):
                filtered_blocks[title] = self._extract_block(block)
            else:
                logging.info("not parsed title: %s", title)

        return filtered_blocks

    def _extract_block(self, filtered_block: Tag) -> Dict[str, Union[List[str], str]]:
        more_sites_button = filtered_block.find("a", class_="category-bottom")

        return {
            "count": self._parse_num_from_text(more_sites_button.text),
            "url": more_sites_button.attrs["href"],
        }

    @staticmethod
    def _parse_num_from_text(text: str) -> int:
        matched = re.match(num_regex, text)
        if matched:
            return int(matched.group(1))
        return 0  # pragma: no cover
