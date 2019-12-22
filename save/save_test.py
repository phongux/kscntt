import sys
sys.path.insert(0,"F:/wsgi/kscntt")
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from beaker.middleware import SessionMiddleware
import json
import config.conn
import hashlib
import datetime
import config.login
import config.sess
import re
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')


def delete_row(table, rowid):
    connect = config.conn.Connect()
    con = connect.get_connection()
    cur = con.cursor()
    cur.execute(f"delete from {table} where id = %s""", (int(rowid),))
    con.commit()
    cur.close()
    con.close()


def update_row(i, table, post, types):
    if post['update[%s][column]' % i] == 'account_password':
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute("update " + table + " set " + post[
            'update[%s][column]' % i] + """ = NULLIF(%s,''), update_time = %s where id = %s """,
                    (hashlib.sha512(
                        post['update[%s][value]' % i].encode('utf-8')).hexdigest(),
                     datetime.datetime.today(), post['update[%s][id]' % i]))
        con.commit()
        cur.close()
        con.close()

    else:
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        if types[post['update[%s][column]' % i]] == 'integer':
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + """ = NULLIF(%s,'')::int, update_time = %s  where id = %s """,
                        (post['update[%s][value]' % i], datetime.datetime.today(),
                         post['update[%s][id]' % i]))
        elif types[post['update[%s][column]' % i]] == 'bigint':
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + """ = NULLIF(%s,'')::bigint, update_time = %s  where id = %s """,
                        (post['update[%s][value]' % i], datetime.datetime.today(),
                         post['update[%s][id]' % i]))
        elif types[post['update[%s][column]' % i]] == 'numeric':
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + """ = NULLIF(%s,'')::numeric, update_time = %s  where id = %s """,
                        (post['update[%s][value]' % i], datetime.datetime.today(),
                         post['update[%s][id]' % i]))
        elif types[post['update[%s][column]' % i]] == 'json':
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + """ = NULLIF(%s,'')::json, update_time = %s  where id = %s """,
                        (json.dumps(post['update[%s][value]' % i]),
                         datetime.datetime.today(), post['update[%s][id]' % i]))
        elif re.search('time',types[post['update[%s][column]' % i]]) or re.search('date', types[post['update[%s][column]' % i]]):
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + """ = NULLIF(%s,'')::timestamp, update_time = %s  where id = %s """,
                        (post['update[%s][value]' % i],
                         datetime.datetime.today(), post['update[%s][id]' % i]))

        else:
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + """ = NULLIF(%s,''), update_time = %s  where id = %s """,
                        (post['update[%s][value]' % i], datetime.datetime.today(),
                         post['update[%s][id]' % i]))
        con.commit()
        cur.close()
        con.close()


def insert_row(i, table, post, types, inscols):
    values = ()
    for colname in inscols:
        if colname == 'account_password':
            values += ("NULLIF('" + hashlib.sha512(
                post['insert[%s][%s]' % (i, colname)].encode(
                    'utf-8')).hexdigest() + "','')",)
        elif types[colname] == 'integer':
            values += (
                "NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                           "''") + "','')::integer",)
        elif types[colname] == 'bigint':
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')::bigint",)
        elif types[colname] == 'numeric':
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')::numeric",)
        elif types[colname] == 'json':
            values += ("NULLIF('" + json.dumps(
                post['insert[%s][%s]' % (i, colname)].replace("'", "''")) + "','')::json",)
        elif re.search('time' , types[colname]) or re.search('date', types[colname]):
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')::timestamp",)
        else:
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')",)
    logging.info(values)
    connect = config.conn.Connect()
    con = connect.get_connection()
    cur = con.cursor()
    cur.execute("""insert into """ + table + """ (""" + ",".join(
        inscols) + """) values ( """ + ",".join(values) + """)""")
    con.commit()
    cur.close()
    con.close()

def insert_undo(i, table, post, types, inscols):
    values = ()
    for colname in inscols:
        if colname == 'account_password':
            values += ("NULLIF('" + hashlib.sha512(
                post['insert[%s][%s]' % (i, colname)].encode(
                    'utf-8')).hexdigest() + "','')",)
        elif types[colname] == 'integer':
            values += (
                "NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                           "''") + "','')::integer",)
        elif types[colname] == 'bigint':
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')::bigint",)
        elif types[colname] == 'numeric':
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')::numeric",)
        elif types[colname] == 'json':
            values += ("NULLIF('" + json.dumps(
                post['insert[%s][%s]' % (i, colname)].replace("'", "''")) + "','')::json",)
        elif re.search('time' , types[colname]) or re.search('date', types[colname]):
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')::timestamp",)
        else:
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')",)

    connect = config.conn.Connect()
    con = connect.get_connection()
    cur = con.cursor()
    cur.execute("""insert into """ + table + """ (""" + ",".join(
        inscols) + """) values ( """ + ",".join(values) + """)""")
    con.commit()
    cur.close()
    con.close()

def delete_check(post, table):
    if 'delete[]' in post:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(delete_row, table, rowid) for rowid in
                       list(post.getall('delete[]')) if rowid != '']
            wait(futures)


def update_check(post, table, types):
    if 'lenupdate' in post:
        if int(post['lenupdate']) > 0:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(update_row, i, table, post, types) for i in
                           range(int(post['lenupdate']))]
                wait(futures)


def insert_check(post, table, types, cols):
    inscols = [col for col in cols if col not in ['id', 'update_time']]
    if 'leninsert' in post:
        if int(post['leninsert']) > 0:
            with ThreadPoolExecutor(max_workers=1) as executor:
                futures = [executor.submit(insert_row, i, table, post, types, inscols) for i in
                           range(int(post['leninsert']))]
                wait(futures)


def undo_check(post, table, types, cols):
    if 'lenundo' in post:
        if int(post['lenundo']) > 0:
            with ThreadPoolExecutor(max_workers=1) as executor:
                futures = [executor.submit(insert_undo, i, table, post, types, cols) for i in
                           range(int(post['lenundo']))]
                wait(futures)

def application(environment, start_response):
    from webob import Request, Response
    request = Request(environment)
    params = request.params
    post = request.POST
    res = Response()
    # Get the session object from the environ
    session = environment['beaker.session']
    login = config.login.Login()
    # Check to see if a value is in the session
    # user = 'username' in session
    if 'username' not in session:
        page = login.login_again()
        response = Response(body=page,
                            content_type="text/html",
                            charset="utf8",
                            status="200 OK")

    elif 'password' not in session:
        page = login.login_again()
        response = Response(body=page,
                            content_type="text/html",
                            charset="utf8",
                            status="200 OK")
    else:
        user = session['username']
        passwd = session['password']
        captcha = session['captcha']
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(
            "select username,account_password,account_level from account where username=%s and account_password=%s and captcha=%s ",
            (user, passwd, captcha))
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()

        if ps[0][2] > 0:
            pass
    if 'cols[]' not in post:
        cols = []
    else:
        cols = post.getall('cols[]')
    types = {}
    connect = config.conn.Connect()
    con = connect.get_connection()
    cur = con.cursor()
    table = 'test'
    cur.execute(
        f"select column_name, data_type from information_schema.columns where table_name = '{table}'")
    rows = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    for row in rows:
        types[row[0]] = row[1]

    # cur.execute("select * from %s limit 1"%table)
    # cols = [desc[0] for desc in cur.description]

    # cols = [desc[0] for desc in rows]

    page = ""
    errors = ""
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(delete_check, post, table),
                   executor.submit(update_check, post, table, types),
                   executor.submit(insert_check, post, table, types, cols),
                   executor.submit(undo_check, post, table, types, cols),
                   ]
        wait(futures)
    page = f"""{{"result":"ok"}}"""
        # else:
        #     page = login.login_again()
    response = Response(body=page,
                        content_type="application/json",
                        charset="utf8",
                        status="200 OK")
    return response(environment, start_response)


sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
