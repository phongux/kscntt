import asyncio
import asyncpg
import logging
class Database:

    def __init__(self):
        self.dsn = """user='postgres',host='localhost',password='RaP202@RaP',port=5432"""
        self.pool = None

    async def connect(self):
        """Initialize asyncpg Pool"""
        self.pool = await asyncpg.create_pool(dsn=self.dsn, min_size=2, max_size=4)
        logging.info("successfully initialized database pool")

