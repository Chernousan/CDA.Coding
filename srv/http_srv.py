#  -*- coding: utf-8 -*-
""" Project: srv | File: http_srv.py | Created: 9/24/23, 1:01 AM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import sys
from http.server import SimpleHTTPRequestHandler
from srv.data import db_instance
from srv.enums import TABLE_TEMPLATE, FINISH_TEMPLATE, START_TEMPLATE


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

        response = db_instance.select()

        html_file = self.get_html(response, enc)

        # Prepare response
        self.send_response(200)
        self.send_header('Content-type', f'text/html; charset={enc}')
        self.send_header('Content-Length', str(len(html_file)))
        self.end_headers()
        # send response
        self.wfile.write(bytes(html_file))

    @staticmethod
    def get_html(data: list, enc: str) -> bytes:
        """
        Generate html document depends on data from DB
        :param enc: str
        :param data: list
        :return: html document
        """
        # convert db table into html table
        table = []
        idx = 1
        for item in data:
            table.append(TABLE_TEMPLATE.format(index=idx, title=item.title, url=item.url))
            idx += 1

        result = [START_TEMPLATE.format(enc), *table, FINISH_TEMPLATE]

        return '\n'.join(result).encode(enc)
