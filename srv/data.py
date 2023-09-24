#  -*- coding: utf-8 -*-
""" Project: srv | File: data.py | Created: 9/22/23, 7:21 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import dataclasses
import time
from typing import Any
import psycopg2
from srv.enums import LIMIT_RETRIES, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, DELETE_Q, \
    SELECT_Q, INSERT_Q


@dataclasses.dataclass
class EstateClass:
    """
    Helper class for data serialization
    """
    title: str
    url: str


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

    def init(self):
        """
        initialization Class
        """
        self.connect()
        self.cursor()

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
                print(f"got error {str(error).strip()}. reconnecting {retry_counter}")
                time.sleep(5)
                self.connect(retry_counter)

            except (Exception, psycopg2.Error) as error:
                raise error

        return None

    def cursor(self) -> [Any, None]:
        """
        Returns the cursor for db
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
        Executing a database query.
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

            retry_counter += 1
            print(f"got error {str(error).strip()}. retrying {retry_counter}")
            time.sleep(1)
            self.reset()
            self.execute(query, retry_counter)

        except (Exception, psycopg2.Error) as error:
            raise error

        # return data only if SELECT query
        if 'SELECT' in query:
            return map(lambda i: EstateClass(*i), self._cursor.fetchall())

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

    def delete(self):
        """
        Delete all data from db
        """
        # delete all data from table
        self.execute(DELETE_Q, LIMIT_RETRIES)

    def select(self) -> Any:
        """
        Get data from db
        """
        return self.execute(SELECT_Q, LIMIT_RETRIES)

    def insert(self, item: Any):
        """
        Insert data
        :param item: Any
        """
        self.execute(INSERT_Q.format(item.title, item.url))


# Declare variable of class DBConnector
db_instance = DBConnector()
