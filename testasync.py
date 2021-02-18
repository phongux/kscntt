import asyncio
import asyncpg

async def run():
    conn = await asyncpg.connect(user='postgres',password='RaP202@RaP',database='kscntt',host='localhost')
    values = await conn.fetch('select *from account')
    await conn.close()
    return values


async def application(environment, start_response):
    from webob import Response
    test = await run()
    page = f"""
        <!doctype html>
        <html>
            <head>
                <title> Login </title>
            </head>
        <body>
            <p> test </p>
        </body>
    </html>"""

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environment, start_response)

asyncio.run(application(environment='',start_response=''))