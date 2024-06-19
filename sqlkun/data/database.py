import aiosqlite
import os

async def connect_db():
    db_path = "./share.db"
    if not os.path.exists(db_path):
        open(db_path, mode="w")
    conn: aiosqlite.Connection = await aiosqlite.connect(db_path)
    return conn

class Database:
    def __init__(self, bot, conn):
        self.bot = bot
        self.main: aiosqlite.Connection = conn

    async def fetchrow(self, sql, *place):
        main = self.main
        cursor = await main.execute(sql, *place)
        row = await cursor.fetchone()
        await cursor.close()
        return row
    
    async def fetch(self, sql, *place):
        main = self.main
        cursor = await main.execute(sql, *place)
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

    async def execute(self, sql, parameters: tuple = None):
        cursor = await self.main.cursor()
        await cursor.execute(sql, parameters)
        await self.main.commit()
        results = await cursor.fetchall()
        description = cursor.description
        await cursor.close()
        return results, description
        