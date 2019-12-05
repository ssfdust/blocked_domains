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


import trio
from loguru import logger
from tqdm import tqdm

from .crawlers.index import IndexCrawler
from .crawlers.cate import MoreSiteCrawler
from .crawlers.sites import SiteListCrawler
from .crawlers.ads import get_combine_crawler
from .const import PORNDUDE
from .utils import chunks


async def start_site_crawler(records):
    urls = set()
    length = len(records) / 53
    logger.warning(f"总批次为{length}")
    for idx, chunk in enumerate(chunks(records, 53)):
        logger.warning(f"开始爬取第{idx + 1}批次")
        for item in chunk:
            logger.info(item)
        sc = SiteListCrawler(chunk)
        await sc.load_website()
        sc.parse()
        urls = urls | sc.urls
        logger.warning("当前批次爬取完毕，10秒后爬取下一批次")
        await trio.sleep(10)

    return urls


async def start_crawler():
    logger.warning("开始爬取主页")
    crawler = IndexCrawler(PORNDUDE)
    await crawler.load_website()
    crawler.parse()

    logger.warning("开始爬取子页")
    ic = MoreSiteCrawler(crawler.extract)
    await ic.load_website()
    ic.parse()
    records = ic.to_records()

    urls = await start_site_crawler(records)

    combine = await get_combine_crawler()
    with open("adult", "w") as f:
        for ele in urls:
            f.write(ele)
            f.write("\n")
    with open("ads", "w") as f:
        for ele in combine.records:
            f.write(ele)
            f.write("\n")


trio.run(start_crawler)
