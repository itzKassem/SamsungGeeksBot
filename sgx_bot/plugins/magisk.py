# (c) 2021 KassemSYR || SamsungGeeksBot

from requests import get
from pyrogram import Client, filters


@Client.on_message(filters.command(["magisk", "root"]))
async def magisk(bot, update):
    url = "https://raw.githubusercontent.com/topjohnwu/magisk_files/"
    message = "Latest Magisk Releases:\n"
    for magisk_type, path in {
        "Stable": "master/stable",
        "Beta": "master/beta",
        "Canary": "canary/canary",
    }.items():
        canary = (
            "https://github.com/topjohnwu/magisk_files/raw/canary/"
            if magisk_type == "Canary"
            else ""
        )
        data = get(url + path + ".json").json()
        message += (
            f"<b>• {magisk_type}</b>:\n"
            f'- <a href="{canary + data["app"]["link"]}">APP - v{data["app"]["version"]}</a> \n'
            f'- <a href="{canary + data["uninstaller"]["link"]}">Uninstaller- {magisk_type}</a> \n'
        )
    await bot.send_message(
        chat_id=update.chat.id, text=message, disable_web_page_preview=True
    )


plugin_name = "Magisk"
plugin_help = """
- /magisk or /root: get latest magisk
              """
