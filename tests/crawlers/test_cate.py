#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from blocked_domain_generator.crawlers.cate import MoreSiteCrawler
from blocked_domain_generator import const


@pytest.mark.second
@pytest.mark.trio
async def test_indirect_crawler(request):
    extract = request.config.cache.get("index", {})
    more_site_crawler = MoreSiteCrawler(extract)
    more_site_crawler.node_tuple_lst = more_site_crawler.node_tuple_lst[:10]
    await more_site_crawler.load_website()
    more_site_crawler.parse()
    records = more_site_crawler.to_records()
    assert records
    extract = request.config.cache.set("records", records[:10])


@pytest.mark.trio
async def test_moresite_crawler(fakedata, monkeypatch):
    monkeypatch.setattr(const, "PORNDUDE_PREFIX", "")
    more_site_crawler = MoreSiteCrawler(fakedata)
    await more_site_crawler.load_website()
