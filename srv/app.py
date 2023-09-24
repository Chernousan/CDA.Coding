#  -*- coding: utf-8 -*-
""" Project: srv | File: app.py | Created: 9/22/23, 7:21 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import socketserver
from srv.helpers import spider_run
from srv.data import db_instance
from srv.enums import SRV_PORT
from srv.http_srv import HttpServer


if __name__ == '__main__':
    print('Application started. Wait for the data to load.')

    # Cleaning the database
    db_instance.delete()

    # Receiving data from the server
    spider_run()
    print('Data reloaded')

    # Starting the http server
    httpd = socketserver.TCPServer(("", SRV_PORT), HttpServer)
    print(f'Serving on http://localhost:{SRV_PORT}')
    httpd.serve_forever()
