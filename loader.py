from pyrogram import Client
from config import config


app = Client(
    name="AutoJoinBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    workers=50,
    sleep_threshold=30,
    in_memory=False
)
