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
    blocked_domain_generator.crawlers.ads
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    完整的广告爬虫
"""
from typing import Set, List
from itertools import chain
from blocked_domain_generator.crawlers.base import MultiCrawler
from blocked_domain_generator.utils import combine_set, difference_set
from blocked_domain_generator.crawlers.file import (
    BanListCrawler,
    HostCrawler,
    FileCrawler,
)
from blocked_domain_generator.const import BlockListFiles
from blocked_domain_generator.crawlers.base import Crawler


class CombineAdCrawler(MultiCrawler):
    def __init__(self, crawlers: List[Crawler], blank_crawler: FileCrawler):
        super().__init__(crawlers)
        self.blank_crawler = blank_crawler

    def _start_loop(self, nursery):
        for crawler in chain(self.crawlers, [self.blank_crawler]):
            nursery.start_soon(crawler.load_website)

    def parse(self):
        for crawler in chain(self.crawlers, [self.blank_crawler]):
            crawler.parse()

    def _combine(self) -> Set:
        args = [crawler.extract for crawler in self.crawlers]
        return combine_set(*args)

    def records(self) -> Set:
        return difference_set(self._combine(), self.blank_crawler.extract)


async def get_combine_crawler() -> CombineAdCrawler:
    """组合三个AD和一个blank ad"""
    crawlers = [
        BanListCrawler(BlockListFiles.banlist),
        HostCrawler(BlockListFiles.hosts),
        FileCrawler(BlockListFiles.v2ray),
    ]
    blank_crawler = FileCrawler(BlockListFiles.ad_blank)

    combine_crawler = CombineAdCrawler(crawlers, blank_crawler)
    await combine_crawler.load_website()
    combine_crawler.parse()

    return combine_crawler
