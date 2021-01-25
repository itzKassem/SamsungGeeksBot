# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

from requests import get
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sgx_bot.utils.devices import GetDevice
from ujson import loads


@Client.on_message(filters.command(["ofx", "orangefox", "fox", "ofx_recovery"]))
async def ofx(bot, update):
    if not len(update.command) == 2:
        message = "Please write your codename into it, i.e <code>/ofx herolte</code>"
        await bot.send_message(
            chat_id=update.chat.id, text=message, disable_web_page_preview=True
        )
        return
    device = update.command[1]
    data = GetDevice(device).get()
    if data:
        name = data["name"]
        device = data["device"]
        brand = data["brand"]
    else:
        message = "coudn't find your device, chack device & try!"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    page = get(
        f"https://api.orangefox.download/v2/device/{device}/releases/stable/last"
    )
    if page.status_code == 404:
        message = f"OrangeFox currently is not avaliable for <code>{device}</code>"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    else:
        message = f"<b>Latest OrangeFox Recovery For {device}</b>\n"
        message += f"<b>Device:</b> <code>{brand.upper()} {name.upper()}</code>\n"
        page = loads(page.content)
        dl_file = page["file_name"]
        version = page["version"]
        size = page["size_human"]
        dl_link = page["url"]
        date = page["date"]
        md5 = page["md5"]
        message += f"<b>Version:</b> <code>{version}</code>\n"
        message += f"<b>Size:</b> <code>{size}</code>\n"
        message += f"<b>Date:</b> <code>{date}</code>\n"
        message += f"<b>File:</b> <code>{dl_file.upper()}</code>\n"
        message += f"<b>MD5:</b> <code>{md5}</code>\n\n"
        keyboard = [[InlineKeyboardButton(text="Download", url=dl_link)]]
        await bot.send_message(
            chat_id=update.chat.id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


plugin_name = "OrangeFox"
plugin_help = """
- /ofx or /orangefox (codename): get latest OrangeFox.
              """
