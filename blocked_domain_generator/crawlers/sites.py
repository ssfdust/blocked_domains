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
    blocked_domain_generator.crawlers.sites
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    站点爬虫
"""
from typing import List, Dict

from trio._core._run import NurseryManager

from blocked_domain_generator.crawlers.base import NameCrawler, MultiCrawler, httpx, global_client
from blocked_domain_generator.parsers.sites import TargetSiteParser
from blocked_domain_generator import const


def new_client() -> httpx.Client:
    return httpx.Client(
        backend=httpx.TrioBackend(),
        timeout=httpx.TimeoutConfig(const.TIMEOUT),
        pool_limits=httpx.PoolLimits(soft_limit=6, hard_limit=100),
    )


class TargetSiteCrawler(NameCrawler, TargetSiteParser):
    def __init__(self, url: str, name: str, client: httpx.Client = global_client):
        NameCrawler.__init__(self, url, name, client)
        TargetSiteParser.__init__(self)


class SiteListCrawler(MultiCrawler):
    def __init__(self, records: List[Dict[str, str]]):
        MultiCrawler.__init__(self)
        self.crawlers: List[TargetSiteCrawler] = []
        self.records = records
        self.client = new_client()
        self.urls = set()

    def _start_loop(self, nursery: NurseryManager):
        for record in self.records:
            name = "{}-{}".format(record["name"], record["title"])
            crawler = TargetSiteCrawler(
                name=name, url=const.PORNDUDE_PREFIX + record["url"],
                client=self.client
            )
            self.crawlers.append(crawler)
            nursery.start_soon(crawler.load_website)

    def parse(self):
        for crawler in self.crawlers:
            crawler.parse()
            self.urls.add(crawler.extract)
