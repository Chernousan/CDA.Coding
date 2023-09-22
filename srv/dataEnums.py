#  -*- coding: utf-8 -*-
""" Project: srv | File: dataEnums.py | Created: 9/22/23, 7:21 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

# List of enums used in application
DB_NAME = 'database'
DB_USER = 'username'
DB_PASS = 'secret'
DB_HOST = 'db'
DB_PORT = '5432'
LIMIT_RETRIES = 5
DOC_TEMPLATE = '''<!DOCTYPE html><html><body><table style="width:100%">{table}</table></body></html>'''
TABLE_TEMPLATE = '<tr><td>{title}</td><td><img src="{url}"></img></td></tr>'
SCRAP_DEPTH = 500
SCRAP_SRC = 'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=1&per_page={0}'
DELETE_Q = "DELETE FROM estate"
SELECT_Q = "SELECT * FROM estate"
INSERT_Q = "INSERT INTO estate (title, url) VALUES ( '{0}', '{1}');"