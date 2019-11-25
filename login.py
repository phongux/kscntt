# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, """F:/wsgi/kscntt""")
from beaker.middleware import SessionMiddleware
import json
import requests
import hashlib
import time
import config.conn
import config.sess
import config.login
import config.module
import importlib
importlib.reload(config.module)
importlib.reload(config.sess)
importlib.reload(config.login)
importlib.reload(config.conn)

def application(environ, start_response):
    from webob import Request, Response
    request = Request(environ)
    post = request.POST
    login = config.login.Login()

    # Get the session object from the environ
    session = environ['beaker.session']
    # Check to see if a value is in the session
    api_url = 'https://www.google.com/recaptcha/api/siteverify'
    site_key = '6LdQQmQUAAAAAIX6RkWjiN7AaswBrFw73HMlMAw4'
    secret_key = '6LdQQmQUAAAAAGhiipTy057aMWHnPuLkEQet8pDy'
    # Set some other session variable

    r = requests.get(f"{api_url}?secret={secret_key}&response={post.get('g-recaptcha-response')}&remoteip={environ.get('HTTP_HOST')}")
    res = json.loads(r.text)

    if not 'username' in post or post['username'] == '' or not 'password' in post \
            or post['password'] == '' or res['success'] == False:
        page = login.login_again()
    else:
        user = post['username']
        passwd = post['password']
        if res['success'] == True:
            module = config.module.Module(user=user, password=passwd, captcha=post['g-recaptcha-response'])
            ps = module.get_account()
            if len(ps) == 0:
                page = login.login_again()
            else:
                session['username'] = user
                session['password'] = hashlib.sha512(passwd.encode('utf-8')).hexdigest()
                session['id'] = ps[0][3]
                session['captcha'] = post['g-recaptcha-response']
                module.update_captcha()
                session.save()
                page = f"""
                        <!doctype html>
                        <html>
                                <head>
                                    <meta http-equiv="refresh" content="0; url=/wsgi/im/index"/>
                                    <title> redirect login </title>
                                </head>
                            <body>
                            </body>
                        </html>"""
        else:
            page = login.login_again()

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")

    return response(environ, start_response)


# Configure the SessionMiddleware

sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
