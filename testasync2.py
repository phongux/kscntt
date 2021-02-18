import asyncio
import asyncpg
import config.database
from asyncpg import Record
from typing import List


async def bench_asyncpg_pool():
    page = ""
    # async with asyncpg.create_pool(user='postgres', host='localhost', password='RaP202@RaP', database='kscntt', command_timeout=60) as pool:
    #     async with pool.acquire() as con:
    #         #results: List[Record] = await con.fetch('select * from account')
    #         results = await con.fetch('select *from account')
    #     # await pool.close()
    #     # for res in results:
    #     #     page += str(res[0]['username'])
    #     return str(results)
    pool = await asyncpg.create_pool(user='postgres',host='localhost',password='RaP202@RaP',database='kscntt')
    con = await pool.acquire()
    try:
        await con.fetch('SELECT 1')
    finally:
        await pool.release(con)

async def run():
    conn = await asyncpg.connect(user='postgres',password='RaP202@RaP',database='kscntt',host='localhost',timeout=60)
    values = await conn.fetch('select *from account')
    await conn.close()
    return values
def application(environment, start_response):
    from webob import Response
    # connect = config.database.Database()
    #result = asyncio.run(bench_asyncpg_pool())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    test = loop.run_until_complete(run())

    page = f"""
        <!doctype html>
        <html>
            <head>
                <title> Login </title>
            </head>
        <body>test {test[0]['username']}</p>
        </body>
    </html>"""

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")

    return response(environment, start_response)

