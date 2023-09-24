#  -*- coding: utf-8 -*-
""" Project: srv | File: spider.py | Created: 9/24/23, 1:15 AM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import json
from typing import Any
import scrapy
from scrapy.http import Response
from srv.data import EstateClass
from srv.enums import SCRAP_SRC, SCRAP_DEPTH


class ScrapSpider(scrapy.Spider):
    """
    A Scrapy class used to retrieve information from a web server
    """
    name = 'srealityspider'

    # Source data url
    start_urls = [SCRAP_SRC.format(SCRAP_DEPTH)]

    # Items post processing
    custom_settings = {'ITEM_PIPELINES': {'srv.pipeline.ItemProcessing': SCRAP_DEPTH}}

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """
        The method returns a data generator
        :param response: Any
        """

        # Converting the response to JSON
        data = json.loads(response.text)

        # Crete generator
        for item in data["_embedded"]["estates"]:
            yield EstateClass(item['name'], item['_links']['images'][0]['href'])
