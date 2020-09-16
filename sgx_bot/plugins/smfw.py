# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

from requests import get
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from bs4 import BeautifulSoup

fw_links = {"SAMMOBILE":"https://www.sammobile.com/samsung/firmware/{}/{}/",
            "SAMFW":"https://samfw.com/firmware/{}/{}/",
            "SAMFREW":"https://samfrew.com/model/{}/region/{}/",
           }.items()

@Client.on_message(filters.command(["checkfw", "check", "fw", "getfw"]))
async def check(bot, update):
    if not len(update.command) == 3:
        message = "Please type your device <b>MODEL</b> and <b>CSC</b> into it!\ni.e <code>/fw SM-G975F XSG!</code>"
        await bot.send_message(
                chat_id=update.chat.id,
                text=message)
        return
    cmd,temp,csc = update.command
    model = 'sm-'+temp if not temp.upper().startswith('SM-') else temp
    fota = get(f'http://fota-cloud-dn.ospserver.net/firmware/{csc.upper()}/{model.upper()}/version.xml')
    test = get(f'http://fota-cloud-dn.ospserver.net/firmware/{csc.upper()}/{model.upper()}/version.test.xml')
    if test.status_code != 200:
        message = f"Couldn't find any firmwares for {temp.upper()} - {csc.upper()}, please refine your search or try again later!"
        await bot.send_message(
                chat_id=update.chat.id,
                text=message)
        return
    page1 = BeautifulSoup(fota.content, 'lxml')
    page2 = BeautifulSoup(test.content, 'lxml')
    os1 = page1.find("latest").get("o")
    os2 = page2.find("latest").get("o")
    if page1.find("latest").text.strip():
        pda1,csc1,phone1=page1.find("latest").text.strip().split('/')
        message = f'<b>\nMODEL:</b> <code>{model.upper()}</code>\n<b>CSC:</b> <code>{csc.upper()}</code>\n'
        message += '<b>Latest Avaliable Firmware:</b>\n'
        message += f'• PDA: <code>{pda1}</code>\n• CSC: <code>{csc1}</code>\n'
        if phone1:
            message += f'• Phone: <code>{phone1}</code>\n'
        if os1:
            message += f'• Android: <code>{os1}</code>\n'
        message += '\n'
    else:
        message = f'<b>No public release found for {model.upper()} and {csc.upper()}.</b>\n\n'
    message += '<b>Latest Test Firmware:</b>\n'
    if len(page2.find("latest").text.strip().split('/')) == 3:
        pda2,csc2,phone2=page2.find("latest").text.strip().split('/')
        message += f'• PDA: <code>{pda2}</code>\n• CSC: <code>{csc2}</code>\n'
        if phone2:
            message += f'• Phone: <code>{phone2}</code>\n'
        if os2:
            message += f'• Android: <code>{os2}</code>\n'
    else:
        md5=page2.find("latest").text.strip()
        message += f'• Hash: <code>{md5}</code>\n• Android: <code>{os2}</code>\n\n'
    cmd.split()
    if cmd in ("checkfw", "check"):
        await bot.send_message(
                chat_id=update.chat.id,
                text=message)
    elif cmd in ("getfw", "fw"):
        keyboard = []
        message += "Download from below\n"
        for site_name, fw_link  in fw_links:
            keyboard += [[InlineKeyboardButton(site_name, url=fw_link.format(model.upper(), csc.upper()))]]
        await bot.send_message(
                chat_id=update.chat.id,
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard))

plugin_name = "Firmware"
plugin_help = """
- /fw or /getfw (device) (csc): get latest firmware.
- /check or /checkfw (device) (csc): check latest firmware.
              """
                