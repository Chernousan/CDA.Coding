#  -*- coding: utf-8 -*-
""" Project: srv | File: http_srv.py | Created: 9/24/23, 1:01 AM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import sys
from http.server import SimpleHTTPRequestHandler
from srv.data import db_instance
from srv.enums import TABLE_TEMPLATE, HTML_TEMPLATE


class HttpServer(SimpleHTTPRequestHandler):
    """
    HTTP implementation class
    """

    def do_GET(self):
        """
        Override function get
        """
        # get encoding
        enc = sys.getfilesystemencoding()

        # Get html file
        html_file = self.get_html(enc)

        # Prepare response
        self.send_response(200)
        self.send_header('Content-type', f'text/html; charset={enc}')
        self.send_header('Content-Length', str(len(html_file)))
        self.end_headers()

        # send response
        self.wfile.write(bytes(html_file))

    @staticmethod
    def get_html(enc: str) -> bytes:
        """
        Generate html document depends on data from DB
        :param enc: str
        :return: html document
        """
        # Get data from db
        table_raw = db_instance.select()

        # convert data to html table
        html_table = ''
        for idx, item in enumerate(table_raw):
            html_table += TABLE_TEMPLATE.format(index=idx, title=item.title, url=item.url)

        return HTML_TEMPLATE.format(enc=enc, table=html_table).encode(enc)
