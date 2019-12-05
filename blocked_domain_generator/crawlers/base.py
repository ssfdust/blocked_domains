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

"""
    blocked_domain_generator.crawler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    基础爬虫类
"""

import sys
import secrets
import socket
import ssl
from typing import List

import trio
import httpx
import tqdm

from httpx.concurrency.trio import TrioBackend
from httpx.exceptions import ConnectTimeout, ReadTimeout
from httpx.config import PoolLimits, TimeoutConfig

from h2.exceptions import StreamClosedError

from trio._core._run import NurseryManager
from trio._channel import MemorySendChannel, MemoryReceiveChannel
from loguru import logger
from blocked_domain_generator.const import (
    RequestState,
    MAX_TRIES,
    TIMEOUT,
    SUCCESS,
    TOO_MANY_REQUESTS,
)

FORMAT = (
    "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> "
    "| <lvl>{level}</lvl> | <lvl>{message}</lvl>"
)
logger.remove()
logger.add(sys.stdout, format=FORMAT, level="WARNING")

limit = trio.CapacityLimiter(4)

global_client = httpx.Client(
    backend=TrioBackend(),
    timeout=TimeoutConfig(TIMEOUT),
    pool_limits=PoolLimits(soft_limit=6, hard_limit=100),
)

ConnectErrors = (
    socket.gaierror,
    trio.BrokenResourceError,
    ConnectTimeout,
    StreamClosedError,
    ssl.SSLError,
    ReadTimeout,
)


class Crawler:
    def __init__(self, url: str, client: httpx.Client = global_client):
        self.url: str = url
        self.data: str = None
        self.client = client
        self.cnt = 0

    async def load_website(self):
        async with self.client as client:
            async with limit:
                logger.info(f"开始爬取{self.url}")
                # Attemp to prevent too many requests
                # at the same time
                await trio.sleep(secrets.randbelow(1000) / 1000)
                await self._retry_loop(client)

    async def load_website_with_sender(self, send_channel):
        async with send_channel:
            await self.load_website()
            logger.debug("Send Finish Signal")
            await send_channel.send("Finish")

    async def _retry_loop(self, client: httpx.Client):
        for _ in range(0, MAX_TRIES):
            state = await self._single_request(client)
            if state is RequestState.Ok:
                break
        else:
            logger.error("%s 爬取彻底失败" % self.url)
            raise RuntimeError("爬取失败")

    async def _single_request(self, client: httpx.Client):
        try:
            self.cnt += 1
            response = await client.get(self.url)
        except ConnectErrors:
            await self._handle_failed(httpx.Response(65536))
        else:
            return await self._handle_response(response)

    async def _handle_response(self, response: httpx.Response) -> int:
        if response.status_code == SUCCESS:
            return self._handle_ok(response)
        return await self._handle_failed(response)

    def _handle_ok(self, response: httpx.Response) -> int:
        logger.info("%s 爬取完毕" % self.url)
        self.data = response.text[:]
        return RequestState.Ok

    async def _handle_failed(self, response: httpx.Response) -> int:
        logger.error("%s 爬取失败 即将重试 第%d次" % (self.url, self.cnt))
        await trio.sleep(0.5)
        if response.status_code == TOO_MANY_REQUESTS:
            hours = float(response.headers["retry-after"]) / 3600
            logger.error("{} 爬取失败，请在{:.2f}小时后重试".format(self.url, hours))
        logger.error(f"{self.url} 错误码{response.status_code}")
        return RequestState.Err


class NameCrawler(Crawler):
    def __init__(self, url: str, name: str, client: httpx.Client = global_client):
        super().__init__(url, client)
        self.name = name


class MultiCrawler:
    def __init__(self, crawlers: List[Crawler] = None):
        self.crawlers = crawlers if crawlers else []
        self.send_channel: MemorySendChannel = None
        self.receive_channel: MemoryReceiveChannel = None
        self.total = len(self.crawlers)
        self.pbar = tqdm.tqdm(total=self.total)
        self.finished = 0

    async def load_website(self):
        async with trio.open_nursery() as nursery:
            self.send_channel, self.receive_channel = trio.open_memory_channel(0)
            await self._start_loop(nursery)
            nursery.start_soon(self._receive_finish)

    async def _receive_finish(self):
        receive_channel = self.receive_channel.clone()
        async with receive_channel:
            async for _ in receive_channel:
                self._update_state()
                if self.finished == self.total:
                    break
            self.pbar.close()

    def _update_state(self):
        self.finished += 1
        self.pbar.update(1)
        logger.debug("{} / {}".format(self.pbar.last_print_n, self.pbar.total))
        logger.debug(f"{self.finished} / {self.total}")

    async def _start_loop(self, nursery: NurseryManager):
        raise NotImplementedError  # pragma: no cover
