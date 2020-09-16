# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

from requests import get
from pyrogram import Client, filters

@Client.on_message(filters.command(["magisk", "root"]))
async def magisk(bot, update):
    url = 'https://raw.githubusercontent.com/topjohnwu/magisk_files/'
    message = "Latest Magisk Releases:\n"
    for magisk_type, path  in {"Stable":"master/stable", "Beta":"master/beta", "Canary (debug)":"canary/debug"}.items():
        data = get(url + path + '.json').json()
        message += f'<b>• {magisk_type}</b>:\nInstaller - <a href="{data["magisk"]["link"]}">v{data["magisk"]["version"]}</a> \n' \
                    f'Manager - <a href="{data["app"]["link"]}">v{data["app"]["version"]}</a> \n' \
                    f'Uninstaller - <a href="{data["uninstaller"]["link"]}">{magisk_type}</a> \n'
    await bot.send_message(
                chat_id=update.chat.id,
                text=message,
                disable_web_page_preview=True
            )

plugin_name = "Magisk"
plugin_help = """
- /magisk or /root: get latest magisk
              """