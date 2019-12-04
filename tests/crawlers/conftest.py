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


@pytest.fixture
def client_with_too_many_requests():
    class Client(httpx.Client):

        async def get(self, url: str) -> httpx.Response:
            return httpx.Response(
                429,
                headers={"retry-after": "3000"}
            )

    return Client()


@pytest.fixture
def client_with_exceptions():
    class Client(httpx.Client):

        async def get(self, url: str) -> httpx.Response:
            raise ConnectTimeout

    return Client()
