# (c) 2021 KassemSYR || SamsungGeeksBot

from requests import get
from pyrogram import Client, filters


@Client.on_message(filters.command(["magisk", "root"]))
async def magisk(bot, update):
    repo_url = "https://raw.githubusercontent.com/topjohnwu/magisk-files/master/"
    message = "Latest Magisk Releases:\n"
    for magisk_type in ["stable", "beta", "canary"]:
        data = get(repo_url + magisk_type + ".json").json()
        message += (
            f"<b>• {magisk_type.capitalize()}</b>:\n"
            f'- <a href="{data["magisk"]["link"]}" >APP - V{data["magisk"]["version"]}</a> \n'
            f'- <a href="{data["magisk"]["note"]}" >Note</a> \n'
        )
    await bot.send_message(
        chat_id=update.chat.id, text=message, disable_web_page_preview=True
    )


plugin_name = "Magisk"
plugin_help = """
- /magisk or /root: get latest magisk
              """
