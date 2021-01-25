# Copyright (C) 2020 - 2020 KassemSYR. All rights reserved.
# This file is part of Galaxy Helper bot.

from sgx_bot import MONGO

# Bot stats
async def stats():
    all_users = MONGO.users.count_documents({})
    return all_users


async def add(userid, username):
    if await is_user(userid) is True:
        return False
    else:
        MONGO.users.insert_one(
            {"_id": userid, "username": username, "lang": "en", "device": None}
        )
        return True


async def is_user(userid):
    is_saved = MONGO.users.find_one({"_id": userid})
    if not is_saved:
        return False
    else:
        return True


# Git
async def get_repos(chatid):
    return MONGO.git.find({"chat_id": chatid})


async def get_repo(chatid, name):
    return MONGO.git.find_one({"chat_id": chatid, "name": name})


async def add_repo(chatid, name, repo):
    found = await get_repo(chatid, name)

    if not found:
        MONGO.git.insert_one({"chat_id": chatid, "name": name, "repo": repo})

        return True
    else:
        MONGO.git.update_one(
            {
                "_id": found["_id"],
                "chat_id": found["chat_id"],
                "name": found["name"],
            },
            {"$set": {"repo": repo}},
        )

        return False


async def delete_repo(chatid, name):
    found = await get_repo(chatid, name)

    if not found:
        return False
    else:
        MONGO.git.delete_one(
            {
                "_id": found["_id"],
                "chat_id": found["chat_id"],
                "name": found["name"],
                "repo": found["repo"],
            }
        )
