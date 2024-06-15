import discord
from sqlkun.data.alldata import *
from sqlkun.other.util import Util
from discord.ext import commands

util = Util()

class OtherCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        try:
            msg =   f"```fix\nコマンド一覧```" \
                    f"```css\n" \
                    f"[{PREFIX}sql (SQL文)]\nSQLを実行します。(100行まで同時実行可能)\n" \
                    f"[{PREFIX}tables]\n現在作成されてるテーブルを取得します。\n" \
                    f"[{PREFIX}views]\n現在作成されてるビューを取得します。\n" \
                    f"[{PREFIX}schema (テーブル名)]\nそのテーブルのスキーマを表示します。\n" \
                    f"[{PREFIX}study]\n30分ごとに勉強しろメンションがbotから飛んでくるようになります。もう一度実行するとリストから除外されます。(00分と30分のとき)\n" \
                    f"[{PREFIX}studies]\n勉強メンションに登録されてるユーザーを取得します。\n" \
                    f"[{PREFIX}randnick]\nランダムなメンバーの名前をあなたのニックネームにします。\n" \
                    f"[{PREFIX}userinfo (ユーザー)]\nユーザーの情報を表示します。引数なしの場合は自分の情報を表示します。\n" \
                    "```" \
                    f"```diff\n- 注意\n- ページ切り替えの最中は別のコマンドを使用できません。必ず処理を停止させてから次のコマンドを使用してください。\n- ここで作成されたDBは利用者に通知せずにリセットすることがあります。\n- 特に権限等は設定していないので無法地帯DBです。データの保証はしません。```"
            embed = discord.Embed(description=msg+"開発者: <@345342072045174795>")
            await ctx.reply(embed=embed)
        except:
            await util.send_traceback(ctx)


    @commands.command()
    async def userinfo(self, ctx, user: discord.Member=None):
        try:
            if not user:
                user = ctx.author
            msg = (
                f"{user.mention}```fix\n名前: {user.global_name}\n"
                f"ニックネーム: {user.display_name}\n"
                f"ユーザーID: {user.name}\n"
                f"ID: {user.id}\n"
                f"作成: {user.created_at.astimezone(timezone(timedelta(hours=+9)))}\n"
                f"参加: {user.joined_at.astimezone(timezone(timedelta(hours=+9)))}\n"
                f"TAG: #{user.discriminator}\n"
                f"システム: {user.system}\n"
                f"BOT: {user.bot}\n"
                f"色: {user.color}\n"
                f"認証: {user.pending}\n"
                f"Nitroブースト日: {None if not user.premium_since else user.premium_since.astimezone(timezone(timedelta(hours=+9)))}\n"
                f"タイムアウト満了: {None if not user.timed_out_until else user.timed_out_until.astimezone(timezone(timedelta(hours=+9)))}\n"
                f"アクティブ名: {None if not user.activities else user.activities[0].name}\n"
                f"ステータス: {user.status}\n"
                f"モバイル: {user.mobile_status}\n"
                f"デスクトップ: {user.desktop_status}\n"
                f"Web: {user.web_status}\n"
                "```"
                )
            embed = discord.Embed(description=msg)
            embed.set_thumbnail(url=user.avatar)
            
            await ctx.reply(embed=embed)
        except:
            await util.send_traceback(ctx)
    


async def setup(bot: commands.Bot):
    await bot.add_cog(OtherCommand(bot))