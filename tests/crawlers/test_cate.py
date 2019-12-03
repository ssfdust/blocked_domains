#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from blocked_domain_generator.crawlers.cate import MoreSiteCrawler


@pytest.mark.second
@pytest.mark.trio
async def test_indirect_crawler(request):
    extract = request.config.cache.get("index", {})
    more_site_crawler = MoreSiteCrawler(extract)
    await more_site_crawler.load_website()
    more_site_crawler.parse()
    records = more_site_crawler.to_records()
    assert records
    extract = request.config.cache.set("records", records)
