import asyncio
import asyncpg
import datetime
# async def fetch_month_data(year,month):
#     "Fetch a month of data from the database"
#     date = datetime.date(year,month,1)
#     connstring = """user='postgres',password='12345678',database='kscntt',host='localhost'"""
#     sql1 = """
#     select date, shares, trades, dollars
#     from factbook
#     where  date <=$1::data
#     and date < $1::date +interval ' 1 month'
#     order by date;
#     """
#     sql = """select *from accounts"""
#
#     pgconn = await asyncpg.connect(connstring)
#     stmt = await pgconn.prepare(sql)
#
#     # res = {}
#     # for (date,shares, trades, dollars) in await stmt.fetch(date):
#     #     res[date] = (shares, trades, dollars)
#     res = await stmt.fetch()
#     await pgconn.close()
#
#     return res

async def run():
    conn = await asyncpg.connect(user='postgres',password='RaP202@RaP',database='kscntt',host='localhost')
    values = await conn.fetch('select *from account')
    await conn.close()
    return str(values[0]['username'])
loop = asyncio.get_event_loop()
test = loop.run_until_complete(run())
print(test)