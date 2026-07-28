import asyncio
import logging
import os
import threading

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from pyrogram import Client, idle

# Load .env (for local development)
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ==========================================
# Telegram Client
# ==========================================

app = Client(
    "AutoJoinRequestBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
)

# ==========================================
# Import Handlers
# ==========================================

import handlers.start
import handlers.callbacks
import handlers.channels
import handlers.join_requests
import handlers.settings
import handlers.admin
import handlers.owner
import handlers.about
import handlers.help
import handlers.welcome

# ==========================================
# FastAPI
# ==========================================

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
    port = int(os.environ.get("PORT", 10000))

    uvicorn.run(
        web,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )


# ==========================================
# Main
# ==========================================

async def main():

    await app.start()

    me = await app.get_me()

    logging.info(
        f"Bot Started Successfully -> @{me.username}"
    )

    print("BOT IS WAITING FOR UPDATES...")
    await idle()

    await app.stop()


if __name__ == "__main__":

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    asyncio.run(main())
