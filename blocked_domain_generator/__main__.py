#!/usr/bin/env python
# -*- coding: utf-8 -*-

import trio
from .crawlers.index import IndexCrawler
from .crawlers.cate import MoreSiteCrawler
from .crawlers.sites import SiteListCrawler
from .crawlers.ads import get_combine_crawler
from .const import PORNDUDE
from .utils import chunks
from loguru import logger


async def start_site_crawler(records):
    urls = set()
    length = len(records)
    logger.info(f"长度为{length}")
    for chunk in chunks(records, 21):
        for item in chunk:
            logger.info(item)
        sc = SiteListCrawler(chunk)
        await sc.load_website()
        sc.parse()
        urls = urls | sc.urls
        logger.info("睡眠30秒")
        await trio.sleep(30)

    return urls


async def start_crawler():
    crawler = IndexCrawler(PORNDUDE)
    await crawler.load_website()
    crawler.parse()

    ic = MoreSiteCrawler(crawler.extract)
    await ic.load_website()
    ic.parse()
    records = ic.to_records()

    urls = await start_site_crawler(records)

    combine = await get_combine_crawler()
    data = combine.records() | urls
    with open("blocked", "w") as f:
        for ele in data:
            f.write(ele)
            f.write("\n")


trio.run(start_crawler)
