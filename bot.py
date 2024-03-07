from config import config
from pyrogram import Client
from pyrogram.enums import ParseMode

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

bot = Client(
    name=config.BOT_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="commands"),
    parse_mode=ParseMode.MARKDOWN
)


scheduler = AsyncIOScheduler(scheduler=BackgroundScheduler(timezone=config.TIME_ZONE))
