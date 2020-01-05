import sys
sys.path.insert(0,"F:/wsgi/kscntt")
from beaker.middleware import SessionMiddleware
import importlib
import re
import json
import config.module
from datetime import datetime
import config.sess
import config.conn
import config.login
hidecols = []
connect = config.conn.Connect()
con = connect.get_connection()
cur = con.cursor()
cur.execute(
    f"select column_name, data_type from information_schema.columns where table_name = 'test' ")
rws = cur.fetchall()
con.commit()
cur.close()
con.close()
cols = []
cols = [desc[0] for desc in rws if desc[0] not in hidecols]
columns = [{},{}]
print(str(columns))