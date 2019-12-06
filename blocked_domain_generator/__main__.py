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

import math
from typing import Set

import trio
from loguru import logger

from .crawlers.index import IndexCrawler
from .crawlers.cate import MoreSiteCrawler
from .crawlers.sites import SiteListCrawler
from .crawlers.ads import get_combine_crawler, FileCrawler
from .const import PORNDUDE, BlockListFiles
from .utils import chunks, get_dist_path, dump_to_dist


async def start_site_crawler(records) -> Set:
    urls = set()
    length = math.floor(len(records) / 53)
    for idx, chunk in enumerate(chunks(records, 53)):
        logger.warning(f"开始爬取第{idx + 1}批次,共{length}批次")
        site_list_crawler = SiteListCrawler(chunk)
        await site_list_crawler.load_website()
        site_list_crawler.parse()
        urls = urls | site_list_crawler.urls
        logger.warning("当前批次爬取完毕，10秒后爬取下一批次")
        await trio.sleep(10)

    return urls

async def start_download_pronlist() -> Set:
    logger.warning("开始下载PornList")
    porn_crawler = FileCrawler(BlockListFiles.porn_list)
    await porn_crawler.load_website()
    porn_crawler.parse()
    return porn_crawler.extract


async def start_adult_crawler() -> Set:
    logger.warning("开始爬取主页")
    crawler = IndexCrawler(PORNDUDE)
    await crawler.load_website()
    crawler.parse()

    logger.warning("开始爬取子页")
    more_sites_crawler = MoreSiteCrawler(crawler.extract)
    await more_sites_crawler.load_website()
    more_sites_crawler.parse()
    records = more_sites_crawler.to_records()

    records = await start_site_crawler(records)
    porn_lst_records = await start_download_pronlist()
    records = records | porn_lst_records

    return records


async def start_ads_crawler() -> Set:
    combine = await get_combine_crawler()
    combine_records = combine.get_records()
    return combine_records


def main():
    dist_path = get_dist_path(create=False)
    concurrency_lst = [start_adult_crawler, start_ads_crawler]
    name_lst = ["adult", "ads"]

    if not dist_path.exists():
        for concurrency, name in zip(concurrency_lst, name_lst):
            records = trio.run(concurrency)
            dump_to_dist(records, name)


main()
