#  -*- coding: utf-8 -*-
""" Project: srv | File: dataClasse.py | Created: 9/22/23, 7:21 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import json
import time
from typing import Any
import psycopg2
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from srv.data_enums import LIMIT_RETRIES, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, DELETE_Q, \
    SCRAP_SRC, SCRAP_DEPTH, INSERT_Q


class EstateClass:
    """
    Helper class for data serialization
    """

    def __init__(self, title, url):
        self.title = title
        self.url = url

    @staticmethod
    def item_list(data: list) -> [None, list]:
        """
        Get serialized data from BD
        :param data: list
        :return: array of class EstateClass
        """
        try:
            return map(lambda i: EstateClass(*i), data) if data else []
        except Exception as error:
            print(str(error))
            return []


class DBConnector:
    """
    Connector for db with "reconnect" function.
    Reconnect function can prevent crash application in case where App docker service started
    before start DB container
    """

    def __init__(self):
        self._connection = None
        self._cursor = None
        self.reconnect = True
        self.init()

    def connect(self, retry_counter: int = 0) -> [None, list]:
        """
        Function that implements the connection to db with retry_counter
        :param retry_counter: int
        :return: [None,list]
        """
        if not self._connection:
            try:
                self._connection = psycopg2.connect(user=DB_USER, password=DB_PASS,
                                                    host=DB_HOST, port=DB_PORT,
                                                    database=DB_NAME, connect_timeout=3)
                retry_counter = 0
                self._connection.autocommit = False
                return self._connection

            except psycopg2.OperationalError as error:
                if not self.reconnect or retry_counter >= LIMIT_RETRIES:
                    raise error

                retry_counter += 1
                print("got error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                time.sleep(5)
                self.connect(retry_counter)

            except (Exception, psycopg2.Error) as error:
                raise error

        return None

    def cursor(self) -> [Any, None]:
        """
        Return cursor fot db
        :return: cursor, None
        """
        if not self._cursor or self._cursor.closed:
            if not self._connection:
                self.connect()
            self._cursor = self._connection.cursor()
            return self._cursor

        return None

    def execute(self, query: str, retry_counter: int = 0) -> [None, list]:
        """
        Return data frm db
        :param query: str
        :param retry_counter: count of reconnect
        :return: None, list
        """
        try:
            self._cursor.execute(query)
            retry_counter = 0

        except (psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            if retry_counter >= LIMIT_RETRIES:
                raise error
            else:
                retry_counter += 1
                print("got error {}. retrying {}".format(str(error).strip(), retry_counter))
                time.sleep(1)
                self.reset()
                self.execute(query, retry_counter)

        except (Exception, psycopg2.Error) as error:
            raise error

        # return data only if SELECT query
        if 'SELECT' in query:
            return EstateClass.item_list(self._cursor.fetchall())

        return None

    def reset(self):
        """
        Reset connection to DB
        """
        self.close()
        self.connect()
        self.cursor()

    def close(self):
        """
        Close connection to DB
        """
        if self._connection:
            if self._cursor:
                self._cursor.close()
            self._connection.close()
            print("PostgresSQL connection is closed")
        self._connection = None
        self._cursor = None

    def init(self):
        """
        initialization Class
        """
        self.connect()
        self.cursor()

    def refresh(self):
        """
        Scrap data from url and store it to the db
        :return: None
        """
        # delete all data from table
        self.execute(DELETE_Q, LIMIT_RETRIES)

        # init Scrapy
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(SRealitySpider)
        # run Scrapy programmatically instead of using cmd
        process.start()


# Declare variable of class DBConnector
db_instance = DBConnector()


class SRealitySpider(scrapy.Spider):
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
            url = ''
            for link in item['_links']['images']:
                url = link['href']
                # stop looping after first element founded
                break

            # store data to DB
            db_instance.execute(INSERT_Q.format(title, url), LIMIT_RETRIES)
