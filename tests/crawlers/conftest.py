#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest
import httpx

from blocked_domain_generator.crawlers.base import ConnectTimeout


@pytest.fixture
def fakedata():
    data = {}
    for i in range(100):
        name = "{}".format(i)
        data[name] = {"count": 1, "url": "https://www.google.com"}
    return data
