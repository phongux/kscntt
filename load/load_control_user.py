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
from config.module import Module
from config.load import Load
import importlib
import math
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
        table = post['table']
        module = Module(user=user, password=passwd, captcha=captcha, table=table)
        ps = module.get_account()
        table_level = module.get_table_account_level()
        if ps[0][2] > 0 and ps[0][2] >= table_level[0][0]:
            if 'display' not in post:
                display = 10
            else:
                display = int(post['display'])
            if 'page' not in post:
                page = 1
            else:
                page = post['page']
            cols = post.getall('cols[]')
            list_cols_str = ",".join(cols)
            start_w = (int(page) - 1) * display
            load = Load(display=display, start_w=start_w, table=table, list_cols_str=list_cols_str)
            rows_count = load.count_rows()
            rows = load.get_rows()
            sum_page = math.ceil(int(rows_count[0]) / display)
            row = []
            for ro in rows:
                row.append(list(ro))
            page = '{"product":'
            objects_list = []
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
            page += f""","sum_page":{int(sum_page)}, "display": {int(display)}, "rows": {int(rows_count[0])}, "log":"{str(ps)};;;;{str(table_level)}"}}"""
        else:
            page = login.login_again()
    response = Response(body=page, content_type="application/json", charset="utf8", status="200 OK")
    return response(environment, start_response)


sess = config.sess.Session()
session_opts = json.loads(sess.session_opts())
application = SessionMiddleware(application, session_opts)
