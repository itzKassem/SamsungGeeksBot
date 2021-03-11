# (c) 2021 KassemSYR || SamsungGeeksBot

from requests import get
from ujson import loads
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sgx_bot.utils.database import get_repos, get_repo, add_repo, delete_repo
from sgx_bot.utils.chat_status import group_admin


@Client.on_message(filters.command(["git"]))
async def git_on_message(bot, update):
    if not len(update.command) == 2:
        message = (
            "Please write release repository into it, i.e <code>/git user/repo</code>"
        )
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    repo = update.command[1]
    page = await check_repo(repo)
    if not page:
        message = "coudn't find any releases on <code>{}</code>".format(repo)
        await bot.send_message(chat_id=update.chat.id, text=message)

    else:
        await git(bot, update, repo, page)


@Client.on_message(filters.command(["repos"]))
async def git_repos(bot, update):
    reply = "There are no saved repositories in this chat"
    message = reply
    repos = await get_repos(update.chat.id)
    for repo in repos:
        if message == reply:
            message = "Repositories saved in this chat:\n"
            message += "<code>!{}</code>\n".format(repo["name"])
        else:
            message += "<code>!{}</code>\n".format(repo["name"])
    await bot.send_message(chat_id=update.chat.id, text=message)


@Client.on_message(filters.command(["fetch"]))
async def fetch_repo(bot, update):
    repo = update.command[1]
    repo_db = await get_repo(update.chat.id, repo)
    if not await get_repo(update.chat.id, repo):
        message = "Repo <b>{}</b> doesn't exist!".format(repo)
        return await bot.send_message(chat_id=update.chat.id, text=message)
    else:
        repo = repo_db["repo"]
        page = get(f"https://api.github.com/repos/{repo}/releases/latest")
        if not page.status_code == 200:
            message = "coudn't find any releases on <code>{}</code>".format(repo)
            await bot.send_message(chat_id=update.chat.id, text=message)

        else:
            await git(bot, update, repo, page)


@Client.on_message(filters.regex(pattern=r"^!\w*"))
async def fetch_legacy(bot, update):
    repo = update.text[1:]
    repo_db = await get_repo(update.chat.id, repo)
    if not await get_repo(update.chat.id, repo):
        message = "Repo <b>{}</b> doesn't exist!".format(repo)
        return await bot.send_message(chat_id=update.chat.id, text=message)
    else:
        repo = repo_db["repo"]
        page = get(f"https://api.github.com/repos/{repo}/releases/latest")
        if not page.status_code == 200:
            message = "coudn't find any releases on <code>{}</code>".format(repo)
            await bot.send_message(chat_id=update.chat.id, text=message)

        else:
            await git(bot, update, repo, page)


@Client.on_message(filters.command(["gitadd"]))
async def save_repo(bot, update):
    status = await group_admin(bot, update)
    if not status:
        return
    if not len(update.command) == 3:
        message = "Please write release repository into it, i.e <code>/gitadd (name) user/repo</code>"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    name = update.command[1]
    repo = update.command[2]
    page = await check_repo(repo)
    if not page:
        message = "Repo have no releases!"
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    msg = "Repo {} successfully. Use <code>/fetch {} </code>to get it"
    if await add_repo(update.chat.id, name, repo) is False:
        message = msg.format("updated", name)
    else:
        message = msg.format("added", name)
    await bot.send_message(chat_id=update.chat.id, text=message)


@Client.on_message(filters.command(["gitdel"]))
async def rm_repo(bot, update):
    if not len(update.command) == 1:
        message = (
            "Please write release repository into it, i.e <code>/gitdel (name)</code>"
        )
        await bot.send_message(chat_id=update.chat.id, text=message)
        return
    status = await group_admin(bot, update)
    if not status:
        return
    name = update.command[1]
    if await delete_repo(update.chat.id, name) == False:
        message = "Repo <b>{}</b> not exists!"
    else:
        message = "Successfully deleted repo: <b>{}</b>"
    await bot.send_message(chat_id=update.chat.id, text=message.format(name))


async def check_repo(repo):
    page = get(f"https://api.github.com/repos/{repo}/releases/latest")
    if not page.status_code == 200:
        return False

    else:
        return page


async def git(bot, update, repo, page):
    db = loads(page.content)
    name = db["name"]
    date = db["published_at"]
    tag = db["tag_name"]
    date = db["published_at"]
    changelog = db["body"]
    dev, repo = repo.split("/")
    message = "<b>Name:</b> <code>{}</code>\n".format(name)
    message += "<b>Tag:</b> <code>{}</code>\n".format(tag)
    message += "<b>Released on:</b> <code>{}</code>\n".format(date[: date.rfind("T")])
    message += "<b>By:</b> <code>{}@github.com</code>\n".format(dev)
    message += "<b>Changelog:</b>\n<code>{}</code>\n\n".format(changelog)
    keyboard = []
    for i in range(len(db)):
        try:
            file_name = db["assets"][i]["name"]
            url = db["assets"][i]["browser_download_url"]
            dls = db["assets"][i]["download_count"]
            size_bytes = db["assets"][i]["size"]
            size = float("{:.2f}".format((size_bytes / 1024) / 1024))
            text = "{}\n💾 {}MB | 📥 {}".format(file_name, size, dls)
            keyboard += [[InlineKeyboardButton(text=text, url=url)]]
        except IndexError:
            continue
    await bot.send_message(
        chat_id=update.chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
    )


plugin_name = "Github"
plugin_help = """
- /git user/repository: get latest releses from repo.
- /repos: get list of saved repisitories in chat.
- /gitadd (name) user/repository: save repository.
- /gitdel (name): delete repository.
- /fetch (name): fetch saved repository, you can also use !(name)
              """
