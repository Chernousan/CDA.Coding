#  -*- coding: utf-8 -*-
""" Project: srv | File: srv.py | Created: 9/22/23, 7:21 PM"""
#  Created by Dmytro Chernousan
#  email: Chernousan@gmail.com
#  Copyright (c) 2023

import io
import sys
import http.server
import socketserver
from dataClass import db_instance
from dataEnums import TABLE_TEMPLATE, SELECT_Q, LIMIT_RETRIES


class HttpServer(http.server.SimpleHTTPRequestHandler):
    """
    HTTP implementation class
    """
    def do_GET(self):
        """
        Override function get
        """
        response = db_instance.execute(SELECT_Q, LIMIT_RETRIES)
        html_file = self.get_html(response)
        self.copyfile(html_file, self.wfile)
        html_file.close()

    def get_html(self, data:list) -> io:
        """
        Generate html document depends on data from DB
        :param data: list
        :return: html document
        """
        # get encoding
        enc = sys.getfilesystemencoding()

        # convert db table into html table
        table = []
        idx = 1
        for item in data:
            table.append(TABLE_TEMPLATE.format(index=idx, title=item.title, url=item.url))
            idx += 1

        result = ['<html><head>'
                  '<meta http-equiv="Content-Type" content="text/html; charset={0}</head><body>">'.format(enc),
                  '<table style="width:100%">',
                  *table,
                  '</table>',
                  '</body></html>']

        encoded = '\n'.join(result).encode(enc)

        # Create HTML file in memory
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)

        # send response
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()

        return f


if __name__ == '__main__':
    print('Application started. Wait for the data to load.')

    # retrieve data form server
    db_instance.refresh()
    print('Data reloaded')

    # start http server
    httpd = socketserver.TCPServer(("", 8000), HttpServer)
    print("Serving on 0.0.0.0:8000 ...")
    httpd.serve_forever()
