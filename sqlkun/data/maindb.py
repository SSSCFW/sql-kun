import aiosqlite
import os

async def connect_db():
    db_path = "./main.db"
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

    async def create_table(self):
        cursor = await self.main.cursor()

        tables = ["CREATE TABLE IF NOT EXISTS study (user_id bigint PRIMARY KEY)"]
        for table in tables:
            await cursor.execute(table)
        await self.main.commit()
        await cursor.close()

    async def add_study_user(self, user_id):
        await self.main.execute(
            "INSERT INTO study VALUES($1)"
            "ON CONFLICT(user_id) DO "
            "UPDATE SET user_id=$1", (user_id,)
        )
        await self.main.commit()

    async def remove_study_user(self, user_id):
        await self.main.execute(
            "DELETE FROM study WHERE user_id=?", (user_id,)
        )
        await self.main.commit()

    async def get_study_user(self, user_id):
        user = await self.fetchrow("SELECT user_id FROM study WHERE user_id=?", (user_id,))
        if not user:
            return 0
        return user[0]