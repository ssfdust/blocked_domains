#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trio
from .crawlers.index import IndexCrawler
from .crawlers.cate import MoreSiteCrawler
from .crawlers.sites import SiteListCrawler
from .crawlers.ads import get_combine_crawler
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
    sc.parse()

    combine = await get_combine_crawler()
    data = combine.records() | sc.urls
    with open("blocked", "w") as f:
        for ele in data:
            f.write(ele)
            f.write("\n")


trio.run(start_crawler)
