import asyncio
import sys
import monkey_patch
from pyrogram import idle
from pyrogram.types import BotCommand

from bot import bot, scheduler


async def start_bot():
    scheduler.start()
    await bot.start()
    await bot.set_bot_commands([
        BotCommand("help", "帮助")
    ])
    try:
        await idle()
    finally:
        await bot.stop()
        sys.exit(0)


if __name__ == '__main__':
    bot.run(start_bot())
