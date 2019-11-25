import hashlib
import sys
sys.path.insert(0,"F:/wsgi/kscntt")
from beaker.middleware import SessionMiddleware
import config.conn
import datetime
import config.login
import config.sess
import json
import re
import logging

logging.basicConfig(level=logging.DEBUG)

def update_rows(post, table, user,id):
    if 'lenupdate' in post:
        if int(post['lenupdate']) > 0:
            for i in range(int(post['lenupdate'])):
                if post['update[%s][column]' % i] == 'username' or post['update[%s][column]' % i] == 'captcha' or post[
                    'update[%s][column]' % i] == 'id' or post['update[%s][column]' % i] == 'account_level':
                    pass
                else:
                    connect = config.conn.Connect()
                    con = connect.get_connection()
                    cur = con.cursor()
                    if post[f'update[{i}][column]'] == 'birthday':
                        cur.execute(f"""update {table} set {post[
                                            'update[%s][column]' % i]} = NULLIF(%s,'')::date, update_time = %s  where id = %s and username=%s """,
                                    (post['update[%s][value]' % i], datetime.datetime.today(), id, user))
                    elif post[f'update[{i}][column]'] == 'account_password':
                        cur.execute("update " + table + " set " + post[
                            'update[%s][column]' % i] + """ = NULLIF(%s,''), update_time = %s where id = %s """,
                                    (hashlib.sha512(
                                        post['update[%s][value]' % i].encode('utf-8')).hexdigest(),
                                     datetime.datetime.today(), post['update[%s][id]' % i]))
                    else:
                        cur.execute(f"""update {table} set {post[
                                            'update[%s][column]' % i]} = NULLIF(%s,''), update_time = %s  where id = %s and username=%s """,
                                    (post['update[%s][value]' % i], datetime.datetime.today(), id, user))
                    con.commit()
                    cur.close()
                    con.close()

def application(environment, start_response):
    from webob import Request, Response
    request = Request(environment)
    post = request.POST
    login = config.login.Login()
    session = environment['beaker.session']
    if 'username' not in session or 'password' not in session:
        page = login.login_again()
    else:
        user = session['username']
        passwd = session['password']
        captcha = session['captcha']
        id = session['id']
        table = 'account'
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(
            "select username,account_password,account_level from account where username=%s and account_password=%s and captcha=%s and id=%s ",
            (user, passwd, captcha, id))
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        if ps[0][2] > 0:
            update_rows(post, table, user,id)
            page = """{"result":"ok"}"""
        else:
            page = login.login_again()
    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")


    return response(environment, start_response)

sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
