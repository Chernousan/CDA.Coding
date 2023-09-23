#  -*- coding: utf-8 -*-
""" Project: srv | File: srv.py | Created: 9/22/23, 7:21 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import sys
import socketserver
from http.server import SimpleHTTPRequestHandler
from srv.data_class import db_instance
from srv.data_enums import TABLE_TEMPLATE, SELECT_Q, LIMIT_RETRIES, SRV_PORT


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

        response = db_instance.execute(SELECT_Q, LIMIT_RETRIES)
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

        result = ['<html><head><meta http-equiv="Content-Type" content="text/html; ',
                  f'charset={enc}</head><body>"><table style="width:100%">',
                  *table, '</table></body></html>']

        return '\n'.join(result).encode(enc)


if __name__ == '__main__':
    print('Application started. Wait for the data to load.')

    # retrieve data form server
    db_instance.refresh()
    print('Data reloaded')

    # start http server
    httpd = socketserver.TCPServer(("", SRV_PORT), HttpServer)
    print('Serving on http://localhost:8000')
    httpd.serve_forever()
