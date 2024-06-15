import asyncio
import contextlib
import io
import math
import subprocess
import textwrap
import traceback
import discord
import sqlkun.data.database
import sqlkun.data.maindb

from sqlkun.data.alldata import *
from sqlkun.other.util import Util
from discord.ext import commands

util = Util()

class DebugCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: sqlkun.data.database.Database = self.bot.db
        self.maindb: sqlkun.data.maindb.Database = self.bot.maindb


    @commands.command()
    async def pullre(self, ctx):
        try:
            if ctx.author.id not in ADMIN:
                return await ctx.reply(PERMISSION_ERROR_MSG)
            await ctx.message.add_reaction("✅")
            subprocess.run(f"git pull".split(" "), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
            subprocess.run("sudo systemctl restart sqlkun".split(" "), stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
        except:
            await util.send_traceback(ctx)

    @commands.command()
    async def linux(self, ctx, *, msg):
        try:
            if ctx.author.id not in ADMIN:
                return await ctx.reply(PERMISSION_ERROR_MSG)
            await ctx.message.add_reaction("✅")
            result = subprocess.run(msg.split(" "), stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            await ctx.send(embed=discord.Embed(description=result.stdout))
        except:
            await util.send_traceback(ctx)

    @commands.command(name="eval")
    async def _eval(self, ctx):
        try:
            if ctx.author.id not in ADMIN:
                return await ctx.send(PERMISSION_ERROR_MSG)
            _last_result = None
            env = {"bot": self.bot, "ctx": ctx, "channel": ctx.channel, "author": ctx.author, "guild": ctx.guild,
                    "message": ctx.message, "_": _last_result, "db": self.db, "maindb": self.maindb,
                    }
            env.update(globals())
            body = util.cleanup_code(ctx.message.content[6:].lstrip())
            stdout = io.StringIO()
            to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"
            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
            func = env["func"]
            try:
                with contextlib.redirect_stdout(stdout):
                    ret = await func()
            except Exception as _:
                value = stdout.getvalue()
                msg = discord.Embed(title=f"！！ＥＲＲＯＲ！！", description=f"```py\n{value}{util.hide_traceback_path(traceback.format_exc())}```",
                                    color=0xC41415)
                await ctx.send(embed=msg)
            else:
                value = stdout.getvalue()
                try:
                    await ctx.message.add_reaction("\u2705")
                except Exception:
                    pass
                if ret is None:
                    if value:
                        limith = 1900
                        if len(value) >= limith:
                            page = int(math.floor(len(value) / limith)) + 1
                            plist = []
                            for i in range(page): plist.append(i + 1)
                            mes = await ctx.send(f"```py\n{value[:limith]}\n```1/{page}")
                            while True:
                                def c(b):
                                    return b.author.id == ctx.author.id
                                try:
                                    guess = await self.bot.wait_for("message", timeout=120, check=c)
                                except asyncio.TimeoutError:
                                    return await mes.add_reaction("🚫")
                                if guess.content == "x":
                                    return await mes.add_reaction("🚫")
                                if guess.isdigit():
                                    getint = int(guess.content)
                                    if getint in plist:
                                        await util.delete(ctx)
                                        await mes.edit(
                                            content=f"```py\n{value[limith * (getint - 1):limith * getint]}\n```{getint}/{page}")
                        else:
                            await ctx.send(f"```py\n{value}\n```")
                else:
                    _last_result = ret
                    await ctx.send(f"```py\n{value}{ret}\n```")
        except:
            print(
                f"evalコマンドによるエラー:{ctx.message.author.guild.name}: {ctx.message.author.name}:\n------------------------\n{ctx.message.content}\n------------------------")
            return await ctx.reply(embed=discord.Embed(title="Error", description="```py\n"+util.hide_traceback_path(traceback.format_exc())+"```", color=0xff0000))



async def setup(bot: commands.Bot):
    await bot.add_cog(DebugCommand(bot))