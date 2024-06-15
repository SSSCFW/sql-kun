import math
import discord
import aiosqlite
import asyncio
import sqlkun.data.database
import sqlkun.data.maindb

from sqlkun.data.alldata import *
from sqlkun.other.util import Util
from discord.ext import commands

util = Util()

class SQLCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: sqlkun.data.database.Database = self.bot.db
        self.maindb: sqlkun.data.maindb.Database = self.bot.maindb


    @commands.command()
    async def schema(self, ctx, table):
        try:
            table.replace("'", "")
            table.replace('"', "")
            result, _ = await self.db.execute(f"PRAGMA table_info('%s')" % table)
            messages = ["index: 名前 : 型 | Null許容 | デフォルト値 | 主キー"]
            messages.append("-"*len(messages[0]))
            for i in result:
                messages.append(f"{i[0]}: {i[1]} : {i[2]} | {bool(i[3])} | {i[4]} | {bool(i[5])}")
            await ctx.reply("```fix\n"+"\n".join(messages)+"```")
        except:
            await util.send_traceback(ctx)

    @commands.command()
    async def tables(self, ctx):
        try:
            result, _ = await self.db.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
            if not result:
                return await ctx.reply(f"```fix\n[テーブル一覧]``````diff\n- テーブルは存在しません。```")
            max_page = math.ceil(len(result)/10)
            tables_msg, page_msg = util.cleanup_tables(result, 1, max_page)
            msg = await ctx.reply(f"```fix\n[テーブル一覧]\n{tables_msg}```{page_msg}")
            if page_msg:
                add_stop(ctx.author.id)
                while True:
                    try:
                        guess = await self.bot.wait_for("message", timeout=60, check=lambda x: x.author.id == ctx.author.id)
                    except asyncio.TimeoutError:
                        remove_stop(ctx.author.id)
                        return await msg.add_reaction("🚫")
                    if guess.content in STOP:
                        remove_stop(ctx.author.id)
                        return await msg.add_reaction("🚫")
                    if guess.content.isdigit():
                        page = int(guess.content)
                        if 1 <= page <= max_page:
                            tables_msg, page_msg = util.cleanup_tables(result, page, max_page)
                            await util.delete(ctx)
                            await msg.edit(content=f"```fix\n[テーブル一覧]\n{tables_msg}```{page_msg}")    
        except:
            await util.send_traceback(ctx)


    @commands.command()
    async def views(self, ctx):
        try:
            result, _ = await self.db.execute(f"SELECT name FROM sqlite_master WHERE type='view';")
            if not result:
                return await ctx.reply(f"```fix\n[ビュー一覧]``````diff\n- ビューは存在しません。```")
            max_page = math.ceil(len(result)/10)
            views_msg, page_msg = util.cleanup_tables(result, 1, max_page)
            msg = await ctx.reply(f"```fix\n[ビュー一覧]\n{views_msg}```{page_msg}")
            if page_msg:
                add_stop(ctx.author.id)
                while True:
                    try:
                        guess = await self.bot.wait_for("message", timeout=60, check=lambda x: x.author.id == ctx.author.id)
                    except asyncio.TimeoutError:
                        remove_stop(ctx.author.id)
                        return await msg.add_reaction("🚫")
                    if guess.content in STOP:
                        remove_stop(ctx.author.id)
                        return await msg.add_reaction("🚫")
                    if guess.content.isdigit():
                        page = int(guess.content)
                        if 1 <= page <= max_page:
                            views_msg, page_msg = util.cleanup_tables(result, page, max_page)
                            await util.delete(ctx)
                            await msg.edit(content=f"```fix\n[ビュー一覧]\n{views_msg}```{page_msg}")
        except:
            await util.send_traceback(ctx)



    @commands.command()
    async def sql(self, ctx, *, sql):
        try:
            if ctx.author.id in stop_command:
                return await ctx.reply(STOP_ERROR_MSG)
            sql = util.cleanup_code(sql)
            queries = sql.split(";")
            if len(queries) > 100 and ctx.author.id not in ADMIN:
                return await ctx.reply("```diff\n- 同時に実行できるクエリの上限は100行です。```")
            for i in queries:
                if i:
                    result, description = await self.db.execute(i)
            await ctx.message.add_reaction("✅")
            if result:
                max_page = math.ceil(len(result)/10)
                cleanup_str, page_msg = util.cleanup_select(result, description, 1, max_page)
                msg = await ctx.reply(f"```\n{cleanup_str}```{page_msg}")
                if page_msg:
                    add_stop(ctx.author.id)
                    while True:
                        try:
                            guess = await self.bot.wait_for("message", timeout=60, check=lambda x: x.author.id == ctx.author.id)
                        except asyncio.TimeoutError:
                            remove_stop(ctx.author.id)
                            return await msg.add_reaction("🚫")
                        if guess.content in STOP:
                            remove_stop(ctx.author.id)
                            return await msg.add_reaction("🚫")
                        if guess.content.isdigit():
                            page = int(guess.content)
                            if 1 <= page <= max_page:
                                cleanup_str, page_msg = util.cleanup_select(result, description, page, max_page)
                                await util.delete(ctx)
                                await msg.edit(content=f"```py\n{cleanup_str}```{page_msg}")
        except aiosqlite.Error as e:
            await ctx.reply(embed=discord.Embed(title="SQL Error", description=f"```py\n{e}```", color=0xff0000))
        except:
            await util.send_traceback(ctx)


async def setup(bot: commands.Bot):
    await bot.add_cog(SQLCommand(bot))