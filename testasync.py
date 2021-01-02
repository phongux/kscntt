import asyncio
import asyncpg

async def run():
    conn= await asyncpg.connect(user='postgres',password='12345678',database='kscntt',host='localhost')
    values = await conn.fetch('select *from account')
    await conn.close()
    return values


def application(environment, start_response):
    from webob import Response
    loop = asyncio.get_event_loop()
    test = loop.run_until_complete(run())

    page = f"""
        <!doctype html>
        <html>
            <head>
                <title> Login </title>
            </head>
        <body>
            <p> test {test[0]['username']}</p>
        </body>
    </html>"""

    response = Response(body=page,
                        content_type="text/html",
                        charset="utf8",
                        status="200 OK")
    return response(environment, start_response)
