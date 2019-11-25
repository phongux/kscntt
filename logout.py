import sys
sys.path.insert(0,"F:/wsgi/kscntt")
from beaker.middleware import SessionMiddleware
import json
import config.sess

def application(environ, start_response):
	from webob import Request, Response
	# Get the session object from the environ
	session = environ['beaker.session']
	session.delete()
	page = """
		<!doctype html>
			<html>
				<head>
				<meta http-equiv="refresh" content="0; url=/wsgi/im/index"/>
					<title> redirect login </title>
				</head>	
			<body>
			</body>
		</html>"""
	response = Response(body = page,
                      content_type = "text/html",
                      charset = "utf8",
                      status = "200 OK")
	return response(environ, start_response)
# Configure the SessionMiddleware
sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
