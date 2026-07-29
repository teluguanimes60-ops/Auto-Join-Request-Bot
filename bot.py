import asyncio
import logging
import os
import threading

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from pyrogram import Client, idle

from database.mongo import connect_db

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================================================
# Telegram Client
# ==========================================================

app = Client(
    "AutoJoinRequestBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# ==========================================================
# Import All Handlers
# ==========================================================

import handlers

# ==========================================================
# FastAPI
# ==========================================================

web = FastAPI()


@web.get("/")
async def root():
    return {
        "status": "running",
        "bot": "Auto Join Request Bot"
    }


@web.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@web.get("/ping")
async def ping():
    return {
        "message": "pong"
    }


def run_web():
    uvicorn.run(
        web,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        log_level="info"
    )


# ==========================================================
# Main
# ==========================================================

async def main():

    # Connect MongoDB
    await connect_db()
    logging.info("MongoDB Connected")

    # Start Bot
    await app.start()

    # Remove webhook if exists
    try:
        await app.delete_webhook()
        logging.info("Webhook Deleted")
    except Exception as e:
        logging.info(f"Webhook: {e}")

    me = await app.get_me()

    logging.info(
        f"Bot Started Successfully -> @{me.username}"
    )

    logging.info("Waiting for updates...")

    await idle()

    await app.stop()


if __name__ == "__main__":

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    asyncio.run(main())
