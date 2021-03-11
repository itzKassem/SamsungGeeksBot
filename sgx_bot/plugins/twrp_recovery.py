# (c) 2021 KassemSYR || SamsungGeeksBot

from requests import get
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup
from sgx_bot.utils.devices import GetDevice


@Client.on_message(filters.command(["rec", "teamwin", "recovery", "twrp"]))
async def twrp(bot, update):
    if not len(update.command) == 2:
        message = "Please write your codename into it, i.e <code>/twrp herolte</code>"
        await bot.send_message(chat_id=update.chat.id, text=message)
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
    url = get(f"https://eu.dl.twrp.me/{device}/")
    if url.status_code == 404:
        message = f"TWRP currently is not avaliable for <code>{device}</code>"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    else:
        message = f"<b>Latest TWRP Recovery For {device}</b>\n"
        message += f"<b>Device:</b> <code>{brand.upper()} {name.upper()}</code>\n"
        page = BeautifulSoup(url.content, "lxml")
        date = page.find("em").text.strip()
        message += f"<b>Updated:</b> <code>{date}</code>\n"
        trs = page.find("table").find_all("tr")
        row = 2 if trs[0].find("a").text.endswith("tar") else 1
        for i in range(row):
            download = trs[i].find("a")
            dl_link = f"https://eu.dl.twrp.me{download['href']}"
            dl_file = download.text
            size = trs[i].find("span", {"class": "filesize"}).text
        message += f"<b>Size:</b> <code>{size}</code>\n"
        message += f"<b>File:</b> <code>{dl_file.upper()}</code>"
        keyboard = [[InlineKeyboardButton(text="Download", url=dl_link)]]
        await bot.send_message(
            chat_id=update.chat.id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


plugin_name = "Twrp"
plugin_help = """
- /twrp or /recovery (codename): get latest twrp.
              """
