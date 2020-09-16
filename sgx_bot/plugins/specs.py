# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.
import re
from requests import get
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from sgx_bot.utils.devices import GetDevice

@Client.on_message(filters.command(["specs", "spec"]))
async def specs(bot, update):
    if not len(update.command) == 2:
        message = "Please write your codename or model into it,\ni.e <code>/specs herolte</code> or <code>/specs sm-g610f</code>"
        await bot.send_message(
                chat_id=update.chat.id,
                text=message)
        return
    device = update.command[1]
    data = GetDevice(device).get()
    if data:
        name = data['name']
        model = data['model']
        device = name.lower().replace(' ' , '-')
    else:
        message = "coudn't find your device, chack device & try!"
        await bot.send_message(
                chat_id=update.chat.id,
                text=message)
        return
    sfw = get(f'https://sfirmware.com/samsung-{model.lower()}/')
    if sfw.status_code == 200:
        page = BeautifulSoup(sfw.content, 'lxml')
        message = '<b>Device:</b> Samsung {}\n'.format(name)
        res = page.find_all('tr', {'class': 'mdata-group-val'})
        res = res[2:]
        for info in res:
            title = re.findall(r'<td>.*?</td>', str(info))[0].strip().replace('td', 'b')
            data = re.findall(r'<td>.*?</td>', str(info))[-1].strip().replace('td', 'code')
            message += "• {}: <code>{}</code>\n".format(title, data)
        await bot.send_message(
                    chat_id=update.chat.id,
                    text=message)
    else:
        giz = get(f'https://www.gizmochina.com/product/samsung-{device}/')
        if giz.status_code == 404:
            message = "device specs not found in bot databases!"
            await bot.send_message(
                    chat_id=update.chat.id,
                    text=message)
            return
        page = BeautifulSoup(giz.content, 'lxml')
        message = '<b>Device:</b> Samsung {}\n'.format(name)
        for info in page.find_all('div', {'class': 'aps-feature-info'}):
            title = info.find('strong').text
            data = info.find('span').text
            message += "• {}: <code>{}</code>\n".format(title, data)
        await bot.send_message(
                    chat_id=update.chat.id,
                    text=message)
plugin_name = "Specs"
plugin_help = """
- /specs (codename or model): get phone specs.
              """
                 