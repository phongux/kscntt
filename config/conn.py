import sys
#sys.path.append( "D:\\backup_I\\wsgi\\kscntt")

import psycopg2
class Connect:

    def __init__(self, user=None, passwd=None, captcha=None, sql=None,  *args, **kwargs):
        self.conn = "dbname=kscntt user=postgres password=RaP202@RaP host=localhost port=5432"
        self.user = user
        self.passwd = passwd
        self.captcha = captcha
        self.sql = sql

    def get_connection(self):
        connection = psycopg2.connect(self.conn)
        return connection

    def check_account(self):
        con = psycopg2.connect(self.conn)
        cur = con.cursor()
        cur.execute(
            "select username, account_password, account_level,team, account_group, id from account where username=%s and account_password=%s ",
            (self.user, self.passwd,))
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return ps


    def get_acount(self):
        con = psycopg2.connect(self.conn)
        cur = con.cursor()
        cur.execute("select username from account ")
        ps = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        return ps



    def run_execute(self):
        con = psycopg2.connect(self.conn)
        cur = con.cursor()
        cur.execute(self.sql)
        con.commit()
        cur.close()
        con.close()

    def get_execute(self):
        con = psycopg2.connect(self.conn)
        cur = con.cursor()
        cur.execute(self.sql)
        ps = cur.fetchone()
        con.commit()
        cur.close()
        con.close()
        return ps



