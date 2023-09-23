#  -*- coding: utf-8 -*-
""" Project: srv | File: enums.py | Created: 9/22/23, 7:21 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

# List of enums used in application
# Postgres constant
DB_NAME = 'database'
DB_USER = 'username'
DB_PASS = 'secret'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Http server cfg
SRV_PORT = 8080

# Limits of retry connection to DB. Used when Db container started lately srv container.
# Can be increased in case DB container has long time to start
LIMIT_RETRIES = 5

# Postgres sql request templates
DELETE_Q = "DELETE FROM estate"
SELECT_Q = "SELECT * FROM estate"
INSERT_Q = "INSERT INTO estate (title, url) VALUES ( '{0}', '{1}');"

# Templates for create HTML
TABLE_TEMPLATE = '<tr><td>{index}</td><td>{title}</td><td><img src="{url}"></img></td></tr>'

# Scrapy variables.
# Warning do not use huge value for SCRAP_DEPTH it affects the startup time of the application and
# creates a harmful load on the server with the original data
SCRAP_DEPTH = 500

# Source server API
SCRAP_SRC = 'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&' \
            'category_type_cb=1&page=1&per_page={0}'
