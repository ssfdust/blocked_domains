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
    tests.parsers.test_ads
    ~~~~~~~~~~~~~~~~~~~~~~
    广告域名的处理
"""
import pytest

from blocked_domain_generator.parsers.ads import FileParser, BanListParser, HostParser

HOST_RESULT = [
    "0.r.msn.com",
    "1100.adsina.allyes.com",
    "1148.adsina.allyes.com",
    "114.allyes.com",
    "114so.cn",
    "123.sogou.com",
    "1251.adsina.allyes.com",
    "1276.adsina.allyes.com",
    "144.dragonparking.com",
    "154.adsina.allyes.com",
    "161.adsina.allyes.com",
]

BAN_LIST_RESULT = [
    "ad.12306.cn",
    "eclick.baidu.com",
    "entry.baidu.com",
    "hmma.baidu.com",
    "mobads-logs.baidu.com",
    "mobads.baidu.com",
    "mtj.baidu.com",
    "nsclick.baidu.com",
    "static.tieba.baidu.com",
    "ucstat.baidu.com",
    "union.baidu.com",
]

FILE_RESULT = [
    "acs4baichuan.m.taobao.com",
    "api.cupid.iqiyi.com",
    "api.jr.mi.com",
    "bce.baidu.com",
    "data.mistat.xiaomi.com",
    "dfp.suning.com",
    "duiba.com.cn",
    "idm.bce.baidu.com",
    "log.tbs.qq.com",
    "metok.sys.miui.com",
    "o2o.api.xiaomi.com",
    "oth.eve.mdt.qq.com",
    "pcbrowser.dd.qq.com",
    "pdc.micloud.xiaomi.net",
    "pms.mb.qq.com",
    "resolver.msg.xiaomi.net",
    "shenghuo.xiaomi.com",
    "ssac.suning.com",
    "ssl-cdn.static.browser.mi-img.com",
    "stdl.qq.com",
    "t10.baidu.com",
    "t11.baidu.com",
    "t12.baidu.com",
    "tools.3g.qq.com",
]

BAN_LIST_FILE = "tests/data/longlist"

HOST_FILE = "tests/data/hosts"

SIMPLE_FILE = "tests/data/ad_blank"


@pytest.mark.parametrize(
    "parser_cls, path, result",
    [
        (BanListParser, BAN_LIST_FILE, BAN_LIST_RESULT),
        (HostParser, HOST_FILE, HOST_RESULT),
        (FileParser, SIMPLE_FILE, FILE_RESULT),
    ],
)
def test_parser(parser_cls, path, result):
    with open(path) as f:
        parser = parser_cls(f.read())
        parser.parse()
        assert parser.extract == set(result)
