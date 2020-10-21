import sys
sys.path.insert(0, "d:/wsgi/kscntt")
from beaker.middleware import SessionMiddleware
import json
import importlib
import config.sess
import config.login
import config.conn
import config.module
#importlib.reload(config.conn)
#importlib.reload(config.module)

def application(environ, start_response):
    from webob import Response
    page = ""
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
            module = config.module.Module(user=user)
            head = module.head()
            headlink = module.headlink()
            menuadmin = module.menuadmin()
            menuuser = module.menuuser()
            menuhead = module.menuhead()
            menufoot = module.menufoot()

            page = ""
            page += head + headlink
            page += "<title>home page</title>"
            page += \
                """
                    </head>
                    <body>
                """
            page += menuhead
            if int(ps[0][2]) == 2:
                page += menuadmin
            else:
                page += menuuser
            page += menufoot
            page += """
            <br />
            <br />
            <br />
            <br />"""
            page += """<p> You are successfully logged in !</p>"""


    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environ, start_response)

# Configure the SessionMiddleware
sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
