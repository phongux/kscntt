import sys
sys.path.insert(0,"F:/wsgi/kscntt")
from config.module import Module

def application(environment, start_response):
    from webob import Response
    module = Module()
    bootstrap = module.bootstrap
    js = module.js
    page = f"""
        <!doctype html>
        <html>
            <head>
                <title> Login </title>
                <script src="{js}/jquery.js"></script>
                <script src="{js}/poper.js"></script>
                <script src="{bootstrap}/js/bootstrap.js"></script>
                <link rel="stylesheet" href="{bootstrap}/css/bootstrap.css">
                <script src='https://www.google.com/recaptcha/api.js'></script>
                <style>
                    html,
                    body {{
                      height: 100%;
                    }}

                    body {{
                      display: -ms-flexbox;
                      display: flex;
                      -ms-flex-align: center;
                      align-items: center;
                      padding-top: 40px;
                      padding-bottom: 40px;
                      background-color: #f5f5f5;
                    }}
                    
                    .form-signin {{
                      width: 100%;
                      max-width: 330px;
                      padding: 15px;
                      margin: auto;
                    }}
                    .form-signin .checkbox {{
                      font-weight: 400;
                    }}
                    .form-signin .form-control {{
                      position: relative;
                      box-sizing: border-box;
                      height: auto;
                      padding: 10px;
                      font-size: 16px;
                    }}
                    .form-signin .form-control:focus {{
                      z-index: 2;
                    }}
                    .form-signin input[type="email"] {{
                      margin-bottom: -1px;
                      border-bottom-right-radius: 0;
                      border-bottom-left-radius: 0;
                    }}
                    .form-signin input[type="password"] {{
                      margin-bottom: 10px;
                      border-top-left-radius: 0;
                      border-top-right-radius: 0;
                    }}
                    .bd-placeholder-img {{
                        font-size: 1.125rem;
                        text-anchor: middle;
                        -webkit-user-select: none;
                        -moz-user-select: none;
                        -ms-user-select: none;
                        user-select: none;
                    }}
                
                    @media (min-width: 768px) {{
                        .bd-placeholder-img-lg {{
                          font-size: 3.5rem;
                        }}
                    }}
                </style>
            </head>	
        <body class='text-center'>
            <form class="form-signin" action = 'login.py' method='post'>
                <img class="mb-4" src="/docs/4.3/assets/brand/bootstrap-solid.svg" alt="" width="72" height="72">
                <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
                <p> Thông tin điền không hợp lệ hoặc thời gian sử dụng đã quá hạn bạn cần đăng nhập lại.</p>
                <label for="inputEmail" class="sr-only">Email address</label>
                <input type="text" id="inputEmail" class="form-control" name="username" placeholder="User name" required="" autofocus="">
                <label for="inputPassword" class="sr-only">Password</label>
                <input type="password" id="inputPassword" class="form-control" name="password" placeholder="Password" required="">
                <div class="checkbox mb-3">
                    <div class="g-recaptcha" data-sitekey="6LdQQmQUAAAAAIX6RkWjiN7AaswBrFw73HMlMAw4"></div>
                <label>
                    <!--<input type="checkbox" value="remember-me"> Remember me-->
                </label>
              </div>
              <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
              <p class="mt-5 mb-3 text-muted">© 2017-2019</p>
            </form>	
        </body>
    </html>"""

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environment, start_response)
