#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
    tests.cralers.test_crawler
    ~~~~~~~~~~~~~~~~~~~
    测试是否爬取到网站内容
"""
import pytest
import respx

from blocked_domain_generator.crawlers.base import Crawler, ConnectTimeout
from blocked_domain_generator import const


@pytest.mark.trio
async def test_website_loaded():
    crawler = Crawler(const.PORNDUDE)

    await crawler.load_website()

    assert crawler.data is not None and "Porn Dude" in crawler.data


@pytest.mark.trio
@respx.mock
async def test_client_with_exceptions():
    respx.get("http://test_exceptions", content=ConnectTimeout())
    crawler = Crawler("http://test_exceptions")

    with pytest.raises(RuntimeError):
        await crawler.load_website()


@pytest.mark.trio
@respx.mock
@pytest.mark.parametrize(
    "code, headers", [(429, {"retry-after": "3000"}), (500, {})]
)
async def test_resp_error(code, headers):
    respx.get("http://test_resp_error", status_code=code, headers=headers)
    crawler = Crawler("http://test_resp_error")

    with pytest.raises(RuntimeError):
        await crawler.load_website()
