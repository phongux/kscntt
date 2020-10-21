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
import importlib
import math
logging.basicConfig(level=logging.ERROR)

class Load:

    def __init__(self, i=None, row=None, cols=None, table=None, display=None, start_w=None, list_cols_str=None, tablename=None, columnname=None, option_select=None, selected=[], link =[], *args, **kwargs):
        self.i = i
        self.row = row
        self.cols = cols
        self.table = table
        self.display = display
        self.list_cols_str = list_cols_str
        self.start_w = start_w
        self.tablename= tablename
        self.columnname= columnname
        self.option_select = option_select
        self.selected = selected
        self.link = link

    def count_rows(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(f"""select count(*) from {self.table}""")
        rows_count = cur.fetchone()
        con.commit()
        cur.close()
        con.close()
        return rows_count

    def get_rows(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(f"""select {self.list_cols_str} from {self.table} order by id limit {self.display} offset {self.start_w}""")
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return rows

    def get_value_option(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(f"""select select_value from select_value where tablename='{self.tablename}' and columnname='{self.columnname}'""")
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return [item[0] for item in rows]

    def get_ky_thuat(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(f"""select username from account where account_group='nv'""")
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return rows


    def get_nguoi_yeu_cau(self):
        connect = config.conn.Connect()
        con = connect.get_connection()
        cur = con.cursor()
        cur.execute(f"""select username from account where account_group='kh'""")
        rows = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return rows

    def get_option_select(self):
        options = ""
        for item in self.get_value_option():
            if item in self.selected:
                options += f"""<option value="{item}" selected='selected'>{item}</option>"""
            else:
                options += f"""<option value="{item}">{item}</option>"""
        return options

    def convert_option(self):
        options = ""
        for item in self.option_select:
            if item in self.selected:
                options += f"""<option value="{item}" selected='selected'>{item}</option>"""
            else:
                options += f"""<option value="{item}">{item}</option>"""
        return options

    def convert_link(self):
        href = ""
        for item in self.link:
            href += f"""<a href='{item}'>{item.split('/')[-1]}</a>; """
        return href