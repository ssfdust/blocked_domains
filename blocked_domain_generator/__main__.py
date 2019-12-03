#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trio
from .crawlers.index import IndexCrawler
from .crawlers.cate import MoreSiteCrawler
from .crawlers.sites import SiteListCrawler
from .const import PORNDUDE


async def start_crawler():
    crawler = IndexCrawler(PORNDUDE)
    await crawler.load_website()
    crawler.parse()

    ic = MoreSiteCrawler(crawler.extract)
    await ic.load_website()
    ic.parse()
    records = ic.to_records()

    sc = SiteListCrawler(records)
    await sc.load_website()


trio.run(start_crawler)
