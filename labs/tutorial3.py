import asyncio
import time
import config.conn

connect = config.conn.Connect()
conn = connect.get_connection()
cur = conn.cursor()
menuadmin = ""
cur.execute("""Select fid,menu1,link from admin_first_menu order by id""")
ps_admin_menu1 = cur.fetchall()
cur.execute("""Select fid,menu1,link from first_menu order by id""")
ps_menu1 = cur.fetchall()
print(ps_menu1)



