import sys
sys.path.insert(0,"F:/wsgi/kscntt")
import psycopg2

class Connect:

    def __init__(self):
        self.conn = "dbname=kscntt user=postgres password=12345678 host=localhost port=5432"

    def get_connection(self):
        connection = psycopg2.connect(self.conn)
        return connection