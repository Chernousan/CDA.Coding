#  -*- coding: utf-8 -*-
""" Project: srv | File: dataClasse.py | Created: 9/22/23, 7:21 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import time
import psycopg2
import requests

from dataEnums import LIMIT_RETRIES, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, DELETE_Q, SCRAP_SRC, SCRAP_DEPTH, \
    INSERT_Q

ISOLEVEL = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT


class EstateClass:
    """
    Helper class for data serialization
    """

    def __init__(self, title, url):
        self.title = title
        self.url = url

    @staticmethod
    def item_list(data: list) -> list:
        """
        Get serialized data from BD
        :param data:
        :return: array of class EstateClass
        """
        try:
            return map(lambda i: EstateClass(*i), data) if data else []
        except Exception as e:
            return []


class DBConnector():
    """
    Connector for db with "reconnect" function.
    Reconnect function can prevent crash application in case where App docker service started before start DB container
    """

    def __init__(self, user: str, password: str, host: str, port: int, database: str, reconnect: int):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._connection = None
        self._cursor = None
        self.reconnect = reconnect
        self.init()

    def connect(self, retry_counter: int = 0) -> [None, list]:
        """
        Function that implements the connection to db with retry_counter
        :param retry_counter:
        :return: [None,list]
        """
        if not self._connection:
            try:
                self._connection = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                                    port=self.port, database=self.database, connect_timeout=3, )
                retry_counter = 0
                self._connection.autocommit = False
                return self._connection
            except psycopg2.OperationalError as error:
                if not self.reconnect or retry_counter >= LIMIT_RETRIES:
                    raise error
                else:
                    retry_counter += 1
                    print("got error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                    time.sleep(5)
                    self.connect(retry_counter)
            except (Exception, psycopg2.Error) as error:
                raise error

    def cursor(self):
        """
        Return cursor fot db
        :return: cursor
        """
        if not self._cursor or self._cursor.closed:
            if not self._connection:
                self.connect()
            self._cursor = self._connection.cursor()
            return self._cursor

    def execute(self, query: str, retry_counter: int = 0) -> [None, list]:
        """
        Return data frm db
        :param query: str
        :param retry_counter: count of reconnect
        :return:
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
        if 'SELECT' in query:
            return EstateClass.item_list(self._cursor.fetchall())

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
            print("PostgreSQL connection is closed")
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
        self.execute(DELETE_Q, LIMIT_RETRIES)

        response = requests.get(SCRAP_SRC.format(SCRAP_DEPTH))
        response_json = response.json()
        if not response_json:
            return

        for item in response_json["_embedded"]["estates"]:
            title = item['name']
            url = ''
            for link in item['_links']['images']:
                url = link['href']
                break
            self.execute(INSERT_Q.format(title, url), LIMIT_RETRIES)


# Declare variable of class DBConnector
db_instance = DBConnector(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME, reconnect=True)
