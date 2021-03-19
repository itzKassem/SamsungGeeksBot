# (c) 2021 KassemSYR || SamsungGeeksBot

from sgx_bot import logger

from pyrogram import Client
from pyrogram import __version__
from pyrogram.raw.all import layer

from sgx_bot import APP_ID, API_HASH, TOKEN


class SGX_BOT(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            name,
            plugins=dict(root=f"{name}/plugins"),
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TOKEN,
        )

    async def start(self):
        await super().start()

        bot_me = await self.get_me()
        self.set_parse_mode("html")
        logger.info(
            f"Bot based on Pyrogram v{__version__} "
            f"(Layer {layer}) started on @{bot_me.username}. "
        )

    async def stop(self, *args):
        await super().stop()
        logger.info("Bot stopped. Bye.")
