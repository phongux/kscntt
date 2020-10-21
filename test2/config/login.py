import sys
sys.path.insert(0,"d:/wsgi/kscntt")
import config.module

class Login:

    def __init__(self):
        module = config.module.Module()
        self.data = f"{module.project}/login_form"
        self.again = f"{module.project}/login_form_again"
        self.notable_url = f"{module.project}/notable"

    def notable(self):
        notable = f"""<!doctype html>
                <html>
                    <head>
                    <meta http-equiv="refresh" content="0; url={self.notable_url}"/>
                        <title> redirect notable </title>
                    </head>	
                <body>
                </body>
            </html>"""
        return notable

    def loginform(self):
        loginform = f"""<!doctype html>
                <html>
                    <head>
                    <meta http-equiv="refresh" content="0; url={self.data}"/>
                        <title> redirect login </title>
                    </head>	
                <body>
                </body>
            </html>"""
        return loginform

    def login_again(self):
        login_again = f"""<!doctype html>
                <html>
                    <head>
                    <meta http-equiv="refresh" content="0; url={self.again}"/>
                        <title> redirect login </title>
                    </head>	
                <body>
                </body>
            </html>"""
        return login_again
