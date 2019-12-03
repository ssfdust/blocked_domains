#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    tests.cralers.test_crawler
    ~~~~~~~~~~~~~~~~~~~
    测试是否爬取到网站内容
"""
import pytest

from blocked_domain_generator.crawlers.base import Crawler
from blocked_domain_generator import const


@pytest.mark.trio
async def test_website_loaded():
    crawler = Crawler(const.PORNDUDE)

    await crawler.load_website()

    assert crawler.data is not None and "Porn Dude" in crawler.data
