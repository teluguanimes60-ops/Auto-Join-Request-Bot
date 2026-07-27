import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# Telegram API
# ==========================================================

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ==========================================================
# MongoDB
# ==========================================================

MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "AutoJoinBot")

# ==========================================================
# Bot Owner
# ==========================================================

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ==========================================================
# Bot Information
# ==========================================================

BOT_NAME = "Auto Join Request Bot"
BOT_VERSION = "1.0.0"

# ==========================================================
# Defaults
# ==========================================================

DEFAULT_DELAY = 60          # seconds
AUTO_DELETE_TIME = 20       # seconds
MAX_CHANNELS = 100

# ==========================================================
# Validation
# ==========================================================

_required = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "MONGO_URI": MONGO_URI,
    "OWNER_ID": OWNER_ID,
}

_missing = [k for k, v in _required.items() if not v]

if _missing:
    raise RuntimeError(
        "Missing environment variables: "
        + ", ".join(_missing)
    )
