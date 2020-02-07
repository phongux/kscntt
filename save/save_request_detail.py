import sys
import os
sys.path.insert(0, "F:/wsgi/kscntt")
from beaker.middleware import SessionMiddleware
import json
import importlib
import config.sess
import config.login
import config.conn
import config.module
importlib.reload(config.conn)
importlib.reload(config.module)

def application(environ, start_response):
    from webob import Response, Request
    request = Request(environ)
    post = request.POST
    # Get the session object from the environ
    session = environ['beaker.session']
    login = config.login.Login()

    #Check to see if a value is in the session
    if not 'username' in session:
        page = login.login_again()
    elif not 'password' in session:
        page = login.login_again()
    else:
        user = session['username']
        passwd = session['password']
        captcha = session['captcha']
        module = config.module.Module(user=user, password=passwd)
        ps = module.get_account()

        if len(ps) == 0:
            page = login.login_again()
        else:
            dir = r"""c:\\tmp\\"""
            page = ""
            if 'file_dinh_kem' in post:
                filefield = post.getall('file_dinh_kem')
                if not isinstance(filefield, list):
                    filefield = [filefield]
                for fileitem in filefield:
                    # #account = request.headers["account"]
                    # #time = request.headers["time"]
                    if fileitem.filename:
                        # strip leading path from file name to avoid directory traversal attacks
                        fn = os.path.basename(fileitem.filename)
                        open(dir + fn, 'wb').write(fileitem.file.read())
                        page += fn
            page += "<title>home page</title>"
            page += \
                """
                    </head>
                    <body>
                """
            page += """
            <br />
            <br />
            <br />
            <br />"""
            page += f"""<p> You are successfully logged in ! {post},{post['cap_do']}</p>"""


    response = Response(body=page,
                        content_type="text/plain",
                        charset="utf8",
                        status="200 OK")
    return response(environ, start_response)

# Configure the SessionMiddleware
sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
