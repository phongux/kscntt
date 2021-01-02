#!/usr/bin/env python3
import sys
import os
sys.path.append( "/var/www/wsgi-scripts/kscntt/config")


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
            <p> test %s</p>
        </body>
    </html>"""%str(accounts)

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environment, start_response)
