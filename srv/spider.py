#  -*- coding: utf-8 -*-
""" Project: srv | File: spider.py | Created: 9/24/23, 1:15 AM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import json
from typing import Any
import scrapy
from scrapy.http import Response
from srv.data import db_instance
from srv.enums import LIMIT_RETRIES, SCRAP_SRC, SCRAP_DEPTH, INSERT_Q


class ScrapSpider(scrapy.Spider):
    """
    Scrapy class, using for retrieve and parse information from web server
    """
    name = 'srealityspider'
    # initial url w`ll retrieve after Class initialisation
    start_urls = [SCRAP_SRC.format(SCRAP_DEPTH)]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        """
        Override Class method for parsing data from server.
        :param response:
        """

        # convert response to JSON
        data = json.loads(response.text)

        # View data and save it to the database. Data stored in object ["_embedded"]["estates"]
        for item in data["_embedded"]["estates"]:
            # get name from current element
            title = item['name']
            # Get first url to image
            url = item['_links']['images'][0]['href']
            # store data to DB
            db_instance.execute(INSERT_Q.format(title, url), LIMIT_RETRIES)
