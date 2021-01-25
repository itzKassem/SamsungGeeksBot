# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

from sgx_bot import OWNER_ID


async def group_admin(bot, update):
    if not update.chat.type == "private":
        status = (await bot.get_chat_member(update.chat.id, update.from_user.id)).status
        if status in ("creator", "administrator"):
            return True
    elif int(update.from_user.id) == OWNER_ID:
        return True
    else:
        return False


async def owner_cmd(update):
    if int(update.from_user.id) == int(OWNER_ID):
        return True
    else:
        return False
