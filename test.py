#!/usr/bin/env python3
import sys
import os
#sys.path.append( "D:\\backup_I\\wsgi\\kscntt")

import config.conn

def application(environment, start_response):
    from webob import Response
    con = config.conn.Connect()
    accounts = con.get_acount()

    page = f"""
        <!doctype html>
        <html>
            <head>
                <title> Login </title>
            </head>
        <body>
            <p> test %s test</p>
        </body>
    </html>"""

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environment, start_response)
