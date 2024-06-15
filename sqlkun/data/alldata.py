import os
from dotenv import load_dotenv
load_dotenv()
import json
from datetime import timezone, timedelta

TOKEN = os.getenv("TOKEN")
USERS = {
    "ubuntu": os.getenv("USER"),
    "windows": os.getenv("WINUSER"),
    "windows_path": os.getenv("WINPATH")
}

ADMIN = [345342072045174795]
PERMISSION_ERROR_MSG = "```diff\n- あなたはこのコマンドを使えません！```"
STOP_ERROR_MSG = "```diff\n- 別のコマンドが実行途中です。xを送信して処理を終了させてください。```"

STOP = ["x", "X", "×"]
JST = timezone(timedelta(hours=+9), "JST")


settings = json.load(open("json/settings.json"))
PREFIX = settings["prefix"]

stop_command = []

def remove_stop(user_id):
    if user_id in stop_command:
        stop_command.remove(user_id)

def add_stop(user_id):
    if user_id not in stop_command:
        stop_command.append(user_id)
