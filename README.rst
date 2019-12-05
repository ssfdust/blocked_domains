Blocked-domain-generator
==========================
.. image:: https://travis-ci.org/ssfdust/blocked_domains.svg?branch=master
    :target: https://travis-ci.org/ssfdust/blocked_domains
.. image:: https://coveralls.io/repos/github/ssfdust/blocked_domains/badge.svg?branch=master
    :target: https://coveralls.io/github/ssfdust/blocked_domains?branch=master
.. image:: https://api.codacy.com/project/badge/Grade/68eaf0c43db449979b7aec7b0810335a
    :target: https://www.codacy.com/manual/ssfdust/blocked_domains?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ssfdust/blocked_domains&amp;utm_campaign=Badge_Grade
.. image:: https://api.codeclimate.com/v1/badges/75348d26bab648540a6d/maintainability
   :target: https://codeclimate.com/github/ssfdust/blocked_domains/maintainability
   :alt: Maintainability
禁止域名列表生成器，包含一个广告列表和一个18x站点列表

使用
-------------------------
.. code-block:: shell

    $ pip install . --user

    $ block_generator

    $ ls sites/
    ads  adult

    $ ./v2sitedat -dat blocked.dat
    ads
    adult
    sites --> blocked.dat
