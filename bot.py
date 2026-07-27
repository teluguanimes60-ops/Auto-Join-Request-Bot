import asyncio
import logging

from fastapi import FastAPI
import uvicorn
from pyrogram import Client

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    PORT
)

from database.mongo import connect_db

# ==========================
# Logging
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger("AutoJoinBot")


# ==========================
# FastAPI
# ==========================

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "running"}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "bot": "Auto Join Request Bot"
    }


# ==========================
# Telegram Bot
# ==========================

bot = Client(
    "AutoJoinBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


# ==========================
# Load Handlers
# ==========================

def load_handlers():
    from handlers import (
        start,
        admin,
        owner,
        channels,
        join_requests,
        settings,
        callbacks,
    )

    logger.info("Handlers loaded successfully.")


# ==========================
# Start Bot
# ==========================

async def start_bot():
    await connect_db()

    load_handlers()

    await bot.start()

    me = await bot.get_me()

    logger.info(f"Bot Started Successfully")
    logger.info(f"Username : @{me.username}")
    logger.info(f"Name     : {me.first_name}")

    await asyncio.Event().wait()


# ==========================
# Run FastAPI
# ==========================

async def start_web():
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
    )

    server = uvicorn.Server(config)

    await server.serve()


# ==========================
# Main
# ==========================

async def main():
    await asyncio.gather(
        start_bot(),
        start_web(),
    )


if __name__ == "__main__":
    asyncio.run(main())
