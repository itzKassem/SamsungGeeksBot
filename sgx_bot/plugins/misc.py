# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

from requests import get
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sgx_bot.plugins.github import git

guides = {
    "Flashing TWRP": "https://telegra.ph/How-to-install-TWRP-recovery-on-Samsung-Phones-08-06"
}.items()


@Client.on_message(filters.command(["phh", "gsi"]))
async def phh(bot, update):
    repo = "phhusson/treble_experimentations"
    page = get(f"https://api.github.com/repos/{repo}/releases/latest")
    if not page.status_code == 200:
        return
    await git(bot, update, repo, page)


@Client.on_message(filters.command(["gcam", "googlecamera"]))
async def gcam(bot, update):
    message = "<b>Google Camera ports for various android devices.</b>\n"
    url = "https://www.celsoazevedo.com/files/android/google-camera/"
    keyboard = [[InlineKeyboardButton(text="GCAM Downloads", url=url)]]

    await bot.send_message(
        chat_id=update.chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command(["glk", "goodlock"]))
async def glk(bot, update):
    message = "<b>Samsung Good Lock for samsung OneUI Devices.</b>\n"
    url = "https://www.apkmirror.com/apk/samsung-electronics-co-ltd/good-lock-2018/"
    keyboard = [[InlineKeyboardButton(text="Good Lock Downloads", url=url)]]

    await bot.send_message(
        chat_id=update.chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command(["guides", "how"]))
async def guidee(bot, update):
    keyboard = []
    for guide_name, guide_link in guides:
        keyboard += [[InlineKeyboardButton(guide_name, url=guide_link)]]
    await bot.send_message(
        chat_id=update.chat.id,
        text="""
Here are some helpful guides!
             """,
        reply_markup=InlineKeyboardMarkup(keyboard),
        reply_to_message_id=update.message_id,
    )


plugin_name = "Misc"
plugin_help = """
- /phh: get latest phh gsi releases.
- /gcam: get Google Camera Ports.
- /guides: get some useful guides.
- /glk: get samsung good lock.
        """
