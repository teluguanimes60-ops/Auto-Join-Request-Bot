import os
from dotenv import load_dotenv

load_dotenv()


# ===========================
# Telegram API
# ===========================
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")


# ===========================
# MongoDB
# ===========================
MONGO_URI = os.getenv("MONGO_URI", "")


# ===========================
# Owner
# ===========================
OWNER_ID = int(os.getenv("OWNER_ID", "0"))


# ===========================
# Bot
# ===========================
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
BOT_NAME = os.getenv("BOT_NAME", "Auto Join Request Bot")


# ===========================
# Render
# ===========================
PORT = int(os.getenv("PORT", "10000"))


# ===========================
# Force Subscribe
# ===========================
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL", "")


# ===========================
# Logging
# ===========================
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))


# ===========================
# Limits
# ===========================
FREE_CHANNEL_LIMIT = int(os.getenv("FREE_CHANNEL_LIMIT", "5"))
PREMIUM_CHANNEL_LIMIT = int(os.getenv("PREMIUM_CHANNEL_LIMIT", "50"))


# ===========================
# Welcome Message
# ===========================
DEFAULT_WELCOME = (
    "👋 Welcome {mention}!\n\n"
    "Your join request has been accepted automatically."
)
