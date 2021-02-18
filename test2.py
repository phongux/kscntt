import asyncpg
import asyncio
import time
import psycopg2

async def bench_asyncpg_con():
    power = 2
    start = time.monotonic()
    for i in range(1000):
        con = await asyncpg.connect(user='postgres', host='10.1.8.35', password='12345678', database='kscntt')
        await con.fetchval('select 2 ^ $1',power)
        await con.close()

    end = time.monotonic()
    print(end - start)


async def bench_asyncpg_pool():
    pool = await asyncpg.create_pool(user='postgres', host='localhost', password='RaP202@RaP', database='kscntt')
    async with pool.acquire() as con:
        result = await con.fetch('select * from account')
    await pool.close()
    return  result[0]['username']

def psycogp2test():
    power = 2
    start = time.monotonic()
    for i in range(1000):
        con = psycopg2.connect("dbname=kscntt user=postgres password=12345678 host=10.1.8.35 port=5432")
        cur = con.cursor()
        cur.execute(f'select 2 ^ {power}')
        cur.fetchone()
        con.commit()
        cur.close()
        con.close()
    end = time.monotonic()
    print(end-start)


print(asyncio.get_event_loop().run_until_complete(bench_asyncpg_pool()))
#psy: 18.796000000000276
#notpool: 50.96900000000096
#pool: 1.125
#0.031000000000858563
# psycogp2test()