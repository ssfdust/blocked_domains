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
    blocked_domain_generator.const
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    所有的const定义
"""

PORNDUDE = "https://theporndude.com/zh"

PORNDUDE_PREFIX = "https://theporndude.com"

KEY_WORD = [
    "成人",
    "色情",
    "情色",
    "艳照门",
    "AV",
    "偷窥",
    "裸",
    "性爱",
    "三陪",
    "女优",
    "Hentai",
]

CATE_CLASS = "category-container"

DIV_TAG = "div"

CLASS_TAG = "class"

DATA_KEY = "data-category-link"

MAX_TRIES = 3

TIMEOUT = 6

TOO_MANY_REQUESTS = 429

SUCCESS = 200

PAGE_MAIN_CONTAINER = "main-container"

PAGE_CATEGORY_CONTENT = "category-content"

PAGE_WRAPPER = "url_links_wrapper"

TITLE_CLASS = "url_link_title"


class RequestState:

    Ok = 0
    Err = 1


class BlockListFiles:

    banlist = (
        "https://raw.githubusercontent.com/"
        "h2y/Shadowrocket-ADBlock-Rules/"
        "master/sr_top500_banlist_ad.conf"
    )
    hosts = "https://cdn.jsdelivr.net/gh/neoFelhz/neohosts@gh-pages/basic/hosts"
    v2ray = (
        "https://raw.githubusercontent.com/"
        "felix-fly/v2ray-dnsmasq-dnscrypt/"
        "master/config/ad.conf"
    )
    ad_blank = (
        "https://raw.githubusercontent.com/"
        "felix-fly/v2ray-dnsmasq-dnscrypt/"
        "master/config/ad_blank.conf"
    )
