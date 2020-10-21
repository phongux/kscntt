import sys
sys.path.insert(0,"d:/wsgi/kscntt")
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from beaker.middleware import SessionMiddleware
import config.conn
import json
import collections
import config.sess
import logging
import config.login
from config.module import Module
import importlib
import math
logging.basicConfig(level=logging.ERROR)

class Save:

    def __init__(self, table=None, rowid=None, *args, **kwargs):
        self.table = table
        self.rowid = rowid

    def delete_row(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(f"delete from {self.table} where id = %s""", (int(self.rowid),))
        con.commit()
        cur.close()
        con.close()