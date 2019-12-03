#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from blocked_domain_generator.crawlers.sites import SiteListCrawler


@pytest.mark.third
@pytest.mark.trio
async def test_sites(request):
    records = request.config.cache.get("records", {})
    sites_crawlers = SiteListCrawler(records)
    await sites_crawlers.load_website()
