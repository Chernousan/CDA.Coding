#  -*- coding: utf-8 -*-
""" Project: srv | File: pipeline.py | Created: 9/25/23, 9:04 AM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

from dataclasses import dataclass
from typing import Any
from srv.data import db_instance


@dataclass
class ItemProcessing:
    """
    Scrapy class, using for retrieve and parse information from web server
    """

    def process_item(self, item: Any, _) -> Any:
        """
        Processing each item
        :param item: item
        :param _: not used parameter
        :return: item after processing
        """
        db_instance.insert(item)
        return item
