# (c) 2021 KassemSYR || SamsungGeeksBot

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

tools = {
    "Odin": "https://samfw.com/Odin/Odin3-v3.14.1.zip",
    "USB Drivers": "https://samfw.com/Odin/SAMSUNG_USB_Driver_for_Mobile_Phones.zip",
}.items()


@Client.on_message(filters.command(["tools", "odin"]))
async def gettool(bot, update):
    keyboard = []
    for tool_name, tool_link in tools:
        keyboard += [[InlineKeyboardButton(tool_name, url=tool_link)]]
    await bot.send_message(
        chat_id=update.chat.id,
        text="""
Here are some files you might need!
             """,
        reply_markup=InlineKeyboardMarkup(keyboard),
        reply_to_message_id=update.message_id,
    )


plugin_name = "Tools"
plugin_help = """
- /tools: get tools.
              """
