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


@pytest.mark.trio
async def test_client_with_exceptions(client_with_exceptions):
    crawler = Crawler("http://test_exceptions", client_with_exceptions)

    with pytest.raises(RuntimeError):
        await crawler.load_website()


@pytest.mark.trio
async def test_resp_error(client_with_too_many_requests):
    crawler = Crawler("http://test", client_with_too_many_requests)

    with pytest.raises(RuntimeError):
        await crawler.load_website()
