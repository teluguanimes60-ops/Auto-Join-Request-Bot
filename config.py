import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Telegram
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")

    # MongoDB
    MONGO_URI = os.getenv("MONGO_URI", "")
    DATABASE_NAME = "AutoJoinBot"

    # Permanent Owner
    OWNER_ID = int(os.getenv("OWNER_ID", "0"))

    # Web (Render)
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", "10000"))

    # Bot
    BOT_NAME = "AutoJoinBot"
    VERSION = "1.0.0"


config = Config()
