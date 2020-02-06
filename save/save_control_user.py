import sys
sys.path.insert(0, "F:/wsgi/kscntt")
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from beaker.middleware import SessionMiddleware
import json
import config.conn
import hashlib
import datetime
import config.login
import config.sess
from config.module import Module
import re
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')

def delete_row(table, rowid, default_delete):
    sql = f"delete from {table} where id = {int(rowid)} {default_delete}"""
    run = config.conn.Connect(sql=sql)
    run.run_execute()


def update_row(i, table, post, types, ps, not_update, default):
    if post['update[%s][column]' % i] not in not_update:
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        if types[post['update[%s][column]' % i]] == 'integer':
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + f""" = NULLIF(%s,'')::int, update_time = %s, {default} = %s  where id = %s and ({default}='{ps[0][0]}' or {default} is null or {default}='')""",
                        (post['update[%s][value]' % i], datetime.datetime.today(), ps[0][0],
                         post['update[%s][id]' % i]))
        elif types[post['update[%s][column]' % i]] == 'bigint':
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + f""" = NULLIF(%s,'')::bigint, update_time = %s, {default} = %s  where id = %s and ({default}='{ps[0][0]}' or {default} is null or {default}='')""",
                        (post['update[%s][value]' % i], datetime.datetime.today(), ps[0][0],
                         post['update[%s][id]' % i]))
        elif types[post['update[%s][column]' % i]] == 'numeric':
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + f""" = NULLIF(%s,'')::numeric, update_time = %s, {default} = %s  where id = %s and ({default}='{ps[0][0]}' or {default} is null or {default}='')""",
                        (post['update[%s][value]' % i], datetime.datetime.today(), ps[0][0],
                         post['update[%s][id]' % i]))
        elif types[post['update[%s][column]' % i]] == 'json':
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + f""" = NULLIF(%s,'')::json, update_time = %s, {default} = %s  where id = %s and ({default}='{ps[0][0]}' or {default} is null or {default}='')""",
                        (json.dumps(post['update[%s][value]' % i]),
                         datetime.datetime.today(), ps[0][0],
                         post['update[%s][id]' % i]))
        elif re.search('time',types[post['update[%s][column]' % i]]) or re.search('date', types[post['update[%s][column]' % i]]):
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + f""" = NULLIF(%s,'')::timestamp, update_time = %s, {default} = %s  where id = %s and ({default}='{ps[0][0]}' or {default} is null or {default}='')""",
                        (post['update[%s][value]' % i],
                         datetime.datetime.today(), ps[0][0],
                         post['update[%s][id]' % i]))

        else:
            cur.execute("update " + table + " set " + post[
                'update[%s][column]' % i] + f""" = NULLIF(%s,''), update_time = %s, {default} = %s  where id = %s and ({default}='{ps[0][0]}' or {default} is null or {default}='')""",
                        (post['update[%s][value]' % i], datetime.datetime.today(), ps[0][0],
                         post['update[%s][id]' % i]))
        con.commit()
        cur.close()
        con.close()
    else:
        pass

def insert_row(i, table, post, types, inscols, ps, default):
    values = ()
    for colname in inscols:
        if colname == 'account_password':
            values += ("NULLIF('" + hashlib.sha512(
                post['insert[%s][%s]' % (i, colname)].encode(
                    'utf-8')).hexdigest() + "','')",)
        elif colname in [f'{default}']:
            values += ("NULLIF('" + ps[0][0] + "','')",)

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
        elif re.search('time', types[colname]) or re.search('date', types[colname]):
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')::timestamp",)
        else:
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')",)
    sql = """insert into """ + table + """ (""" + ",".join(
        inscols) + """) values ( """ + ",".join(values) + """)"""
    connect = config.conn.Connect(sql=sql)
    connect.run_execute()


def updateall_row(i, table, post, types, cols, default, ps):
    values = []
    cols = [col for col in cols if col not in ['update_time']]
    for colname in cols:
        if colname == 'account_password':
            values.append(colname + " = NULLIF('" + hashlib.sha512(
                post['updateall[%s][%s]' % (i, colname)].encode('utf-8')).hexdigest() + "','')")
        elif types[colname] == 'integer':
            values.append(colname +
                " = NULLIF('" + post['updateall[%s][%s]' % (i, colname)].replace("'", "''") + "','')::integer")
        elif types[colname] == 'bigint':
            values.append(colname + " = NULLIF('" + post['updateall[%s][%s]' % (i, colname)].replace("'", "''") + "','')::bigint")
        elif types[colname] == 'numeric':
            values.append(colname + " = NULLIF('" + post['updateall[%s][%s]' % (i, colname)].replace("'", "''") + "','')::numeric")
        elif types[colname] == 'json':
            values.append(colname + " = NULLIF('" + json.dumps(
                post['insert[%s][%s]' % (i, colname)].replace("'", "''")) + "','')::json")
        elif re.search('time' , types[colname]) or re.search('date', types[colname]):
            values.append(colname + " = NULLIF('" + post['updateall[%s][%s]' % (i, colname)].replace("'", "''") + "','')::timestamp")
        else:
            values.append(colname + " = NULLIF('" + post['updateall[%s][%s]' % (i, colname)].replace("'", "''") + "','')")

    sql = """update """ + table + """ set """ + ",".join(values) + f""", update_time = %s , {default}='{ps[0][0]}'  where id = %s and ({default}='{ps[0][0]}' or {default} is null or {default}='')""", (datetime.datetime.today(), post['updateall[%s][id]' % (i)].replace("'", "''"))
    connect = config.conn.Connect(sql=sql)
    connect.run_execute()

def insert_undo(i, table, post, types, inscols, ps):
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
        elif re.search('time', types[colname]) or re.search('date', types[colname]):
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')::timestamp",)
        else:
            values += ("NULLIF('" + post['insert[%s][%s]' % (i, colname)].replace("'",
                                                                                  "''") + "','')",)
    sql = """insert into """ + table + """ (""" + ",".join(
        inscols) + """) values ( """ + ",".join(values) + """)"""
    connect = config.conn.Connect(sql)
    connect.run_execute()


def delete_check(post, table, ps, default_delete):
    if 'delete[]' in post:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(delete_row, table, rowid, default_delete) for rowid in
                       list(post.getall('delete[]')) if rowid != '']
            wait(futures)


def update_check(post, table, types, ps, not_update, default):
    if 'lenupdate' in post:
        if int(post['lenupdate']) > 0:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(update_row, i, table, post, types, ps, not_update, default) for i in
                           range(int(post['lenupdate']))]
                wait(futures)


def insert_check(post, table, types, cols, ps, inscols, default):
    if 'leninsert' in post:
        if int(post['leninsert']) > 0:
            with ThreadPoolExecutor(max_workers=1) as executor:
                futures = [executor.submit(insert_row, i, table, post, types, inscols, ps, default) for i in
                           range(int(post['leninsert']))]
                wait(futures)

def updateall_check(post, table, types, cols, default, ps):
    if 'lenupdateall' in post:
        if int(post['lenupdateall']) > 0:
            with ThreadPoolExecutor(max_workers=1) as executor:
                futures = [executor.submit(updateall_row, i, table, post, types, cols, default, ps) for i in
                           range(int(post['lenupdateall']))]
                wait(futures)


def undo_check(post, table, types, cols, ps):
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
        table = post['table']
        notinsertcols = ['id', 'update_time', 'ngay']
        default = ""
        not_update = []
        default_conf = {
            "nv": "ky_thuat",
            "kh": "nguoi_yeu_cau"
        }
        not_update_conf ={
            "nv": ["id", "update_time", "y_kien_khach_hang", "ngay"],
            "kh": ["id", "update_time", "huong_xu_ly", "ngay"]
        }

        module = Module(user=user, password=passwd, captcha=captcha, table=table)
        ps = module.get_account()
        table_level = module.get_table_account_level()
        if ps[0][2] > 0 and ps[0][2] >= table_level[0][0]:
            if 'cols[]' not in post:
                cols = []
            else:
                cols = post.getall('cols[]')
            for key, value in default_conf.items():
                if ps[0][4] == key:
                    default = value
            for key, value in not_update_conf.items():
                if ps[0][4] == key:
                    for item in value:
                        not_update.append(item)

            update_default = f"{default}='{ps[0][0]}'"
            inscols = [col for col in cols if col not in notinsertcols]
            default_query = f" and {default}='{ps[0][0]}'"
            types = {}
            rows = module.get_type_columns()

            for row in rows:
                types[row[0]] = row[1]
            # cur.execute("select * from %s limit 1"%table)
            # cols = [desc[0] for desc in cur.description]

            # cols = [desc[0] for desc in rows]

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(delete_check, post, table, ps, default_query),
                           executor.submit(update_check, post, table, types, ps, not_update, default),
                           executor.submit(insert_check, post, table, types, cols, ps, inscols, default),
                           executor.submit(undo_check, post, table, types, cols, ps),
                           executor.submit(updateall_check, post, table, types, cols, ps,default_query)
                           ]
                wait(futures)
            page = f"""{{"result":"ok", "post":"{not_update}, {default}"}}"""
        else:
            page = login.login_again()
    response = Response(body=page,
                        content_type="application/json",
                        charset="utf8",
                        status="200 OK")
    return response(environment, start_response)


sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
