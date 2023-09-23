#  -*- coding: utf-8 -*-
""" Project: srv | File: helpers.py | Created: 9/24/23, 1:13 AM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

from scrapy.crawler import CrawlerProcess
from srv.spider import ScrapSpider


def spider_run():
    """
    Start spider
    """
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(ScrapSpider)
    process.start()
