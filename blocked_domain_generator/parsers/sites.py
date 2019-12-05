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
    blocked_domain_generator.parsers.sites
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    more sites页面的处理器
"""
from typing import Union, List, Dict
from bs4 import Tag, BeautifulSoup

from blocked_domain_generator.parsers.base import BaseParser
from blocked_domain_generator import const
from blocked_domain_generator.utils import drop_schema


class SiteParser(BaseParser):
    def parse(self):
        if self.bs4 is None:
            self.init_parser()
        wrapper = self._resolve_wrapper()
        self.extract = self._resolve_titlelink(wrapper)

    def _resolve_div_element(
        self, node: Union[Tag, BeautifulSoup], next_conditions: List[str]
    ) -> Tag:
        condition = next_conditions.pop()

        target = node.find(const.DIV_TAG, class_=condition)

        if next_conditions:
            return self._resolve_div_element(target, next_conditions)

        return target

    def _resolve_wrapper(self) -> Tag:
        next_conditions = [
            const.PAGE_WRAPPER,
            const.PAGE_CATEGORY_CONTENT,
            const.PAGE_MAIN_CONTAINER,
        ]

        return self._resolve_div_element(self.bs4, next_conditions)

    def _resolve_titlelink(self, tag: Tag) -> List[Dict[str, str]]:
        records = []
        for url_element in tag.find_all(const.DIV_TAG, class_=const.TITLE_CLASS):
            records.append(
                {
                    "name": self.name,
                    "title": url_element.text,
                    "url": url_element.find("a").attrs["href"],
                }
            )

        return records


class TargetSiteParser(BaseParser):
    def parse(self):
        if self.bs4 is None:
            self.init_parser()
        node = self.bs4.find(const.DIV_TAG, "favicon-bar-addressbar")
        self.extract = drop_schema(node.a.attrs["title"])
