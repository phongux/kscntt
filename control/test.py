#! c:/python39/python
import sys
import os
sys.path.insert(1, "d:/wsgi/kscntt")
lib_path = os.path.abspath(os.path.join('config'))
sys.path.append("d:\\wsgi\\kscntt\\config")

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
            <p> test %s test -</p>
        </body>
    </html>"""%str(accounts)

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environment, start_response)
