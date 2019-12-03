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
    blocked_domain_generator.crawlers.cate
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    根据获取到得分类来获取网页
"""
from typing import List, Dict, NewType, Union, Tuple

from loguru import logger
import trio

from blocked_domain_generator.crawlers.base import NameCrawler, MultiCrawler
from blocked_domain_generator.parsers.sites import SiteParser
from blocked_domain_generator import const

ExtractType = NewType("ExtractType", Dict[str, Dict[str, Union[str, List[str]]]])


class SitePageCrawler(NameCrawler, SiteParser):
    def __init__(self, url: str, name: str, count: int):
        NameCrawler.__init__(self, url, name)
        SiteParser.__init__(self)
        self.count = count

    def check_extract_amount(self):
        extract_len = len(self.extract)
        if self.count != extract_len:
            logger.warning(f"{self.name} 总数为{self.count}, 实际{extract_len}")
        else:
            logger.info(f"{self.name} 总数为{self.count}, 全部爬取完毕")


class MoreSiteCrawler(MultiCrawler):
    def __init__(self, cate_nodes: ExtractType):
        super().__init__()
        self.node_tuple_lst = self.flat_nodes(cate_nodes)
        self.extract = None
        self.records = []

    @staticmethod
    def flat_nodes(cate_nodes: ExtractType) -> List[Tuple]:
        node_tuple_lst = []
        for name, node in cate_nodes.items():
            value_box = [name, node["count"], node["url"]]
            node_tuple_lst.append(value_box)

        return node_tuple_lst

    def _start_loop(self, nursery):
        for name, count, url in self.node_tuple_lst:
            crawler = SitePageCrawler(
                url=const.PORNDUDE_PREFIX + url, name=name, count=count
            )
            self.crawlers[name] = crawler
            nursery.start_soon(crawler.load_website)

    def parse(self):
        for _, crawler in self.crawlers.items():
            crawler.parse()
            crawler.check_extract_amount()

    def to_records(self) -> Dict[str, Dict[str, str]]:
        if self.records:
            return self.records
        for crawler in self.crawlers.values():
            self.records.extend(crawler.extract)

        return self.records
