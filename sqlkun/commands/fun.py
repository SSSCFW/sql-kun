import random
import discord
import sqlkun.data.database
import sqlkun.data.maindb

from sqlkun.data.alldata import *
from sqlkun.other.util import Util
from discord.ext import commands

util = Util()

class FunCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: sqlkun.data.database.Database = self.bot.db
        self.maindb: sqlkun.data.maindb.Database = self.bot.maindb

    @commands.command(name="randnick")
    async def random_nickname(self, ctx):
        try:
            mebers = ctx.guild.members
            member: discord.Member = random.choice(mebers)
            name = member.display_name
            try:
                await ctx.author.edit(nick=name)
                await ctx.reply(embed=discord.Embed(description=f"{member.mention}のニックネームに変更しました。"))
            except discord.errors.Forbidden:
                await ctx.reply(embed=discord.Embed(description=f"{ctx.author.mention}のニックネームを変更する権限がありません。\nあなたがギルドオーナーの場合、このコマンドは使えません。"))
        except:
            await util.send_traceback(ctx)

    @commands.command()
    async def study(self, ctx, user: discord.User=None):
        try:
            user_id = ctx.author.id
            if user:
                if user_id not in ADMIN:
                    return await ctx.reply(PERMISSION_ERROR_MSG)
                user_id = user.id
            exist = await self.maindb.get_study_user(user_id)
            msg = ""
            if exist:
                await self.maindb.remove_study_user(user_id)
                msg = f"<@{user_id}>を勉強メンションリストから除外しました。"
            else:
                await self.maindb.add_study_user(user_id)
                msg = f"<@{user_id}>を勉強メンションリストに追加しました！"
            await ctx.reply(embed=discord.Embed(description=msg))
        except:
            await util.send_traceback(ctx)

    @commands.command()
    async def studies(self, ctx):
        try:
            exist = await self.maindb.fetch("SELECT user_id FROM study")
            members = "\n".join(map(lambda x: f"・<@{x}>", [i[0] for i in exist]))
            await ctx.reply(embed=discord.Embed(description=f"勉強メンション対象者\n{members}"))
        except:
            await util.send_traceback(ctx)

    


async def setup(bot: commands.Bot):
    await bot.add_cog(FunCommand(bot))