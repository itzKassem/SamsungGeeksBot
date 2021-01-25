# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

from requests import get
from pyrogram import Client, filters
from sgx_bot.utils.devices import GetDevice
from ujson import loads


@Client.on_message(filters.command(["whatis", "device", "codename", "samsung"]))
async def models(bot, update):
    if not len(update.command) == 2:
        message = "Please write your codename into it, i.e <code>/whatis herolte</code>"
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
        model = data["model"]
    else:
        message = "coudn't find your device, chack device & try!"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    message = f"<b>{device}/{model.upper()}</b> is <code>{brand} {name}</code>\n"
    await bot.send_message(
        chat_id=update.chat.id, text=message, disable_web_page_preview=True
    )


@Client.on_message(filters.command(["variants", "models"]))
async def variants(bot, update):
    if not len(update.command) == 2:
        message = "Please write your codename into it, i.e <code>/specs herolte</code>"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    device = update.command[1]
    data = GetDevice(device).get()
    if data:
        name = data["name"]
        device = data["device"]
    else:
        message = "coudn't find your device, chack device & try!"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    data = get(
        "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/by_device.json"
    ).content
    db = loads(data)
    device = db[device]
    message = f"<b>{name}</b> variants:\n\n"
    for i in device:
        name = i["name"]
        model = i["model"]
        message += (
            "<b>Model</b>: <code>{}</code> \n<b>Name:</b> <code>{}<code>\n\n".format(
                model, name
            )
        )

    await bot.send_message(chat_id=update.chat.id, text=message)


plugin_name = "Devices"
plugin_help = """
- /whatis (codename): get phone neme from codename.
- /variants (codename): get phone variants.
              """
