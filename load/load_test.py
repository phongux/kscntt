import sys
sys.path.insert(0,"F:/wsgi/kscntt")
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from beaker.middleware import SessionMiddleware
import config.conn
import json
import collections
import config.sess
import logging
import config.login
import importlib
logging.basicConfig(level=logging.ERROR)

def convert_row(i, row, cols):
    d = collections.OrderedDict()
    d['idha'] = i + 1  # row[0]
    for j in range(len(cols)):
        if type(row[i][j]).__name__ == 'datetime' or type(row[i][j]).__name__ == 'date':
            d[cols[j]] = str(row[i][j])
        elif type(row[i][j]).__name__ == 'float':
            d[cols[j]] = str(round(row[i][j], 9))
        elif type(row[i][j]).__name__ == 'Decimal':
            d[cols[j]] = str(row[i][j])
        elif type(row[i][j]).__name__ == 'dict' or type(row[i][j]).__name__ == 'list':
            d[cols[j]] = json.dumps(row[i][j], ensure_ascii=False).encode('utf8').decode(
                'utf-8')
        else:
            d[cols[j]] = row[i][j]
    return d


def get_account(user, passwd, captcha):
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
    return ps


def count_rows():
    connect = config.conn.Connect()
    con = connect.get_connection()
    cur = con.cursor()
    cur.execute(f"""select count(*) from test""")
    rows_count = cur.fetchone()
    con.commit()
    cur.close()
    con.close()
    return rows_count


def get_rows(display, start_w):
    connect = config.conn.Connect()
    con = connect.get_connection()
    cur = con.cursor()
    cur.execute(f"""select id,ho,ten,update_time from test order by id""")
    rows = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return rows


def application(environment, start_response):
    from webob import Request, Response
    request = Request(environment)
    # params = request.params
    post = request.POST
    # res = Response()
    session = environment['beaker.session']
    login = config.login.Login()

    if 'username' not in session:
        page = login.login_again()
    elif 'password' not in session:
        page = login.login_again()
    else:
        user = session['username']
        passwd = session['password']
        captcha = session['captcha']
        ps = get_account(user, passwd, captcha)
        if ps[0][2] > 0:
            if 'display' not in post:
                display = 200
            else:
                display = int(post['display'])
            if 'page' not in post:
                page = 1
            else:
                page = post['page']
            start_w = (int(page) - 1) * display
            rows_count = count_rows()
            rows = get_rows(display, start_w)
            sum_page = (int(rows_count[0]) / display) + 1
            row = []
            for ro in rows:
                row.append(list(ro))
            page = '{"product":'
            objects_list = []
            cols = ["id", "ho","ten","update_time"]
            with ThreadPoolExecutor(max_workers=1) as executor:
                futures = [executor.submit(convert_row, i, row, cols) for i in range(len(row))]
                for future in as_completed(futures):
                    try:
                        objects_list.append(future.result())
                    except Exception as exc:
                        logging.error(exc)
                    else:
                        pass
            page += json.dumps(objects_list)
            page += ""","sum_page":%s}""" % (int(sum_page))
        else:
            page = login.login_again()
    response = Response(body=page, content_type="text/html", charset="utf8", status="200 OK")
    return response(environment, start_response)


sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
