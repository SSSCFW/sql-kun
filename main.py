import discord
import sqlkun.data.database
import sqlkun.data.maindb
import datetime


from sqlkun.data.alldata import *
from datetime import datetime
from discord.ext import tasks
from discord.ext import commands

class Main(commands.Bot):
    def __init__(self):
        Intents = discord.Intents.all()
        super().__init__(command_prefix=settings["prefix"], intents=Intents)
        self.bot = self
        self.remove_command("help")  # helpコマンドを削除

    async def setup_hook(self):
        conn = await sqlkun.data.database.connect_db()
        mainconn = await sqlkun.data.maindb.connect_db()
        self.db: sqlkun.data.database.Database = sqlkun.data.database.Database(self, conn)
        self.maindb: sqlkun.data.maindb.Database = sqlkun.data.maindb.Database(self, mainconn)
        await self.maindb.create_table()
        load_command = ("debug", "fun", "other", "sql")
        for cmd in load_command:
            await self.load_extension(f"sqlkun.commands.{cmd}")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Login!")
        print(f"Name: {self.user}\nID: {self.user.id}")
        print("--------")
        gamestatus = discord.Game(f"{PREFIX}help")
        await self.change_presence(status=discord.Status.idle, activity=gamestatus)
        self.study_loop.start()

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload):
        if payload.guild_id == 1241314729209757767:
            user = payload.user
            await self.get_channel(1251364990842044486).send(f"{user.display_name} ({user.name}/{user.id})が退出しました。")

    @tasks.loop(seconds=60)
    async def study_loop(self):
        channel_id = 1241314729209757767
        now = datetime.now(JST) # 現在の時刻
        if now.strftime("%M") in ("00", "30"):
            exist = await self.maindb.fetch("SELECT user_id FROM study")
            if exist:
                members = "\n".join(map(lambda x: f"・<@{x}>", [i[0] for i in exist]))
                await self.get_channel(channel_id).send(f"勉強しろ\n{members}")

bot = Main()
bot.run(TOKEN)