import sys
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
    from webob import Response
    page = ""
    # Get the session object from the environ
    session = environ['beaker.session']
    login = config.login.Login()
    module = config.module.Module()
    #Check to see if a value is in the session
    if not 'username' in session:
        page = login.login_again()
    elif not 'password' in session:
        page = login.login_again()
    else:
        user = session['username']
        passwd = session['password']
        captcha = session['captcha']
        try:
            connect = config.conn.Connect()
            con = connect.get_connection()
            cur = con.cursor()
            cur.execute(
                "select username,account_password,account_level from account where username=%s and account_password=%s and captcha=%s ",
                (user, passwd, captcha))
            ps = cur.fetchall()
            page += str(ps)
            if len(ps) == 0:
                page = login.login_again()
            else:
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
            con.commit()
            cur.close()
            con.close()
        except OSError as err:
            #page = "OS error: {0}".format(err)
            page = "Can not access databases"


    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environ, start_response)

# Configure the SessionMiddleware
sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
