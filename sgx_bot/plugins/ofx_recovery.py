# (c) 2021 KassemSYR || SamsungGeeksBot

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
    page = get(f"https://api.orangefox.download/v2/device/{device}/releases/")

    if page.status_code == 404:
        message = f"OrangeFox currently is not avaliable for <code>{device}</code>"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    else:
        dl_link = "https://dl.orangefox.download/"
        message = f"<b>OrangeFox Recovery Releases For {device}</b>\n"
        message += f"<b>Device:</b> <code>{brand.upper()} {name.upper()}</code>\n"
        res = loads(page.content)
        for release in res["stable"]:
            message += f"<u><b>{release['version']}</b></u>\n"
            message += f"• <b>Date:</b> <code>{release['date']}</code>\n"
            message += f"• <b>ID:</b> <code>{release['_id']}</code>\n"
            message += f"• <b>Download:</b> <i><a href='{dl_link+release['_id']}'>Direct link</a></i>\n\n"
        keyboard = [
            [
                InlineKeyboardButton(
                    text=f"Download Latest ({res['stable'][0]['version']})",
                    url=dl_link + res["stable"][0]["_id"],
                )
            ]
        ]
        await bot.send_message(
            chat_id=update.chat.id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


plugin_name = "OrangeFox"
plugin_help = """
- /ofx or /orangefox (codename): get latest OrangeFox.
              """
