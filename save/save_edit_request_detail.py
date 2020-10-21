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
import shutil
import secrets
from datetime import datetime
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
            con = config.conn.Connect()
            kieu_yeu_cau = post.get('kieu_yeu_cau')
            che_do = post.get('che_do')
            cap_do = post.get('cap_do')
            trang_thai = post.get('trang_thai')
            nguoi_yeu_cau = post.get('nguoi_yeu_cau')
            nhom = post.get('nhom')
            ky_thuat = post.getall('ky_thuat')
            loai_dich_vu = post.get('loai_dich_vu')
            chu_de = post.get('chu_de')
            mo_ta = post.get('mo_ta')
            huong_xu_ly = post.get('huong_xu_ly')
            y_kien_khach_hang = post.get('y_kien_khach_hang')
            table = post.get('table')
            id = post.get('id')
            default_conf = {
                "nv": "ky_thuat",
                "kh": "nguoi_yeu_cau"
            }

            page = ""

            if 'file_dinh_kem' in post and post.get('file_dinh_kem') != b'':
                path = user + secrets.token_urlsafe(22)
                direct = os.path.normpath(f"c:/Apache24/htdocs/kscntt/files/{path}")
                if not os.path.exists(direct):
                    os.mkdir(direct)
                filefield = post.getall('file_dinh_kem')
                if not isinstance(filefield, list):
                    filefield = [filefield]
                for fileitem in filefield:
                    #account = request.headers["account"]
                    #time = request.headers["time"]
                    if fileitem.filename:
                        # strip leading path from file name to avoid directory traversal attacks
                        fn = os.path.basename(fileitem.filename)
                        open(direct + '\\' + fn, 'wb').write(fileitem.file.read())
                        page += fn
                if ps[0][4] == 'nv':
                    con.sql = f"""update {table} set kieu_yeu_cau='{kieu_yeu_cau}', 
                                        che_do='{che_do}', 
                                        cap_do='{cap_do}', 
                                        trang_thai='{trang_thai}', 
                                        nguoi_yeu_cau='{nguoi_yeu_cau}', 
                                        nhom='{nhom}', 
                                        ky_thuat='{{{','.join(ky_thuat)}}}', 
                                        loai_dich_vu='{loai_dich_vu}', 
                                        chu_de='{chu_de}', 
                                        mo_ta='{mo_ta}', 
                                        huong_xu_ly='{huong_xu_ly}',
                                        file_path='{path}' where id={id}  """
                elif ps[0][4] == 'kh':
                    con.sql = f"""update {table} set kieu_yeu_cau='{kieu_yeu_cau}', 
                                        che_do='{che_do}', 
                                        cap_do='{cap_do}', 
                                        trang_thai='{trang_thai}', 
                                        nguoi_yeu_cau='{nguoi_yeu_cau}', 
                                        nhom='{nhom}', 
                                        ky_thuat='{{{','.join(ky_thuat)}}}', 
                                        loai_dich_vu='{loai_dich_vu}', 
                                        chu_de='{chu_de}', 
                                        mo_ta='{mo_ta}', 
                                        huong_xu_ly='{huong_xu_ly}',
                                        y_kien_khach_hang='{y_kien_khach_hang}',
                                        file_path='{path}' where id={id} and nguoi_yeu_cau='{user}' """
                else:
                    con.sql = None
                # old_path = post.get('old_path')
                # if old_path != '' or old_path is not None:
                #     direct = direct + old_path
                #     shutil.rmtree(direct)
            else:
                if ps[0][4] == 'nv':
                    con.sql = f"""update {table} set kieu_yeu_cau='{kieu_yeu_cau}', 
                                che_do='{che_do}', 
                                cap_do='{cap_do}', 
                                trang_thai='{trang_thai}', 
                                nguoi_yeu_cau='{nguoi_yeu_cau}', 
                                nhom='{nhom}', 
                                ky_thuat='{{{','.join(ky_thuat)}}}', 
                                loai_dich_vu='{loai_dich_vu}', 
                                chu_de='{chu_de}', 
                                mo_ta='{mo_ta}', 
                                huong_xu_ly='{huong_xu_ly}' where id={id} """
                elif ps[0][4] == 'kh':
                    con.sql = f"""update {table} set kieu_yeu_cau='{kieu_yeu_cau}', 
                                che_do='{che_do}', 
                                cap_do='{cap_do}', 
                                trang_thai='{trang_thai}', 
                                nguoi_yeu_cau='{nguoi_yeu_cau}', 
                                nhom='{nhom}', 
                                ky_thuat='{{{','.join(ky_thuat)}}}', 
                                loai_dich_vu='{loai_dich_vu}', 
                                chu_de='{chu_de}', 
                                mo_ta='{mo_ta}', 
                                huong_xu_ly='{huong_xu_ly}',
                                y_kien_khach_hang='{y_kien_khach_hang}' where id={id} and nguoi_yeu_cau='{user}' """
                else:
                    con.sql = None
                # old_path = post.get('old_path')
                # if old_path != '' or old_path != None:
                #     direct = direct + old_path
                #     shutil.rmtree(direct)
            con.run_execute()
            page += """
            <html>
            <title>home page</title>
            
            """
            page += \
                f""" <head>
                        <meta http-equiv="refresh" content="0; url=/wsgi/kscntt/control/edit_request_detail?table={table}&id={id}"/>
                    </head>
                    <body>
                """
            page += """
            <br />
            <br />
            <br />
            <br />"""
            page += f"""<p>You are successfully ! </p>
                </html>
            """


    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environ, start_response)

# Configure the SessionMiddleware
sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
