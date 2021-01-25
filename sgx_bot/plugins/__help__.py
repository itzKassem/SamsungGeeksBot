# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import importlib
import re

from sgx_bot.utils.database import stats, add
from sgx_bot.utils.chat_status import owner_cmd
from sgx_bot.utils.help_menu import help_buttons

from sgx_bot.plugins import all_plugins

HELP = {}
for plugin in all_plugins:
    imported_plugin = importlib.import_module("sgx_bot.plugins." + plugin)
    if hasattr(imported_plugin, "plugin_help") and hasattr(
        imported_plugin, "plugin_name"
    ):
        plugin_name = imported_plugin.plugin_name
        plugin_help = imported_plugin.plugin_help
        HELP.update({plugin: [{"name": plugin_name, "help": plugin_help}]})


@Client.on_message(
    filters.command(["start", "start@SamsungGeeksBot", "help@SamsungGeeksBot", "help"])
)
async def start(bot, update):
    userid = update.from_user.id
    name = update.from_user.first_name
    username = update.from_user.username
    usr_bot_me = await bot.get_me()
    bot_username = str(usr_bot_me.username)
    if update.chat.type == "private":
        keyboard = [
            [InlineKeyboardButton("Help!", callback_data="menu")],
            [
                InlineKeyboardButton(
                    "Add me to a group",
                    url="http://telegram.me/{}?startgroup=botstart".format(
                        bot_username
                    ),
                )
            ],
        ]
        text = """
Hey <b>{}</b>!, I'm <b>Galaxy Helper</b>.
feel free to use me, click on help to find out more on how to use me!
             """.format(
            name
        )
        await add(userid, username)
    else:

        keyboard = [
            [
                InlineKeyboardButton(
                    "Go PM!", url="t.me/{}?start=help".format(bot_username)
                )
            ]
        ]
        text = "Hey there, I'm alive!\nCheck my <b>PM</b> for help!"
    await bot.send_message(
        chat_id=update.chat.id,
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        reply_to_message_id=update.message_id,
    )


async def help_menu(bot, update):
    await update.answer(text="Choose a plugin to get help!")
    keyboard = InlineKeyboardMarkup(help_buttons(HELP))
    text = """
Hi, <b>I'm Galaxy helper!</b> an all-in-one telegram bot for Samsung users!
I can get you latest Official Firmware, Root, Specs, Or Twrp, and many more things!
To know more on how to use me check this list!
             """
    await update.message.edit_caption(caption=text, reply_markup=keyboard)


async def help_plugin(bot, update, text):
    keyboard = [[InlineKeyboardButton("Back", callback_data="menu")]]
    text = "<b> Avaliable Commands:</b>\n" + text
    await update.message.edit_caption(
        caption=text, reply_markup=InlineKeyboardMarkup(keyboard)
    )


@Client.on_message(filters.command(["stats"]))
async def send_stats(bot, update):
    status = await owner_cmd(update)
    if not status:
        return
    users = await stats()
    await bot.send_message(
        chat_id=update.chat.id,
        text="I currently have {} users in my db".format(users),
        reply_to_message_id=update.message_id,
    )


@Client.on_callback_query(filters.regex("menu"))
async def button(bot, update: CallbackQuery):
    await help_menu(bot, update)


@Client.on_callback_query(filters.regex(pattern=".*help_plugin.*"))
async def but(bot, update: CallbackQuery):
    plug_match = re.match(r"help_plugin\((.+?)\)", update.data)
    plug = plug_match.group(1)
    text = str(HELP[plug][0]["help"])
    name = str(HELP[plug][0]["name"])
    await update.answer(text=name + " Help!")
    await help_plugin(bot, update, text)
