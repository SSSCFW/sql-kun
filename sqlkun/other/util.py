import traceback
import discord
from sqlkun.data.alldata import *

class Util:
    def hide_traceback_path(self, traceback):
        traceback = traceback.replace("C:\\Users\\"+USERS["windows"]+"\\", "User\\")
        traceback = traceback.replace("c:\\Users\\"+USERS["windows"]+"\\", "User\\")
        traceback = traceback.replace("/home/"+USERS["ubuntu"], "/home/User")
        traceback = traceback.replace(USERS["windows_path"], "sql-kun")
        return traceback
    
    async def send_traceback(self, ctx):
        await ctx.reply(embed=discord.Embed(title="Error", description="```py\n"+self.hide_traceback_path(traceback.format_exc())+"```", color=0xff0000))
        print(f"{ctx.message.content.split()[0]} -------\n{traceback.format_exc()}")

    def cleanup_select(self, select, description, page=1, max_page=1):
        description = [d[0] for d in description]
        result = [" | ".join(description)]
        result.append("-"*len(result[0]))
        for i in select[(page-1)*10:page*10]:
            result.append(" | ".join(map(str, i)))
        page_msg = ""
        if max_page != 1:
            page_msg = f"```fix\n{page} / {max_page} (数値送信で切り替え | xで終了)```"
        return "\n".join(result), page_msg

    def cleanup_tables(self, tables, page=1, max_page=1):
        result = "\n".join(map(lambda x: str(x[0]), tables[(page-1)*10:page*10]))
        page_msg = ""
        if max_page != 1:
            page_msg = f"```fix\n{page} / {max_page} (数値送信で切り替え | xで終了)```"
        return result, page_msg

    def cleanup_code(self, content):
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])
        return content.strip("` \n")

    async def delete(self, ctx):
        async for msg in ctx.channel.history(limit=1):
            if msg.author == ctx.author:
                return await msg.delete()