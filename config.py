import os
from dotenv import load_dotenv

# Load .env locally (ignored on Render if not present)
load_dotenv()

# ===========================
# Telegram API
# ===========================

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ===========================
# Database
# ===========================

MONGO_URI = os.getenv("MONGO_URI", "")

# ===========================
# Owner
# ===========================

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ===========================
# Bot Settings
# ===========================

BOT_NAME = "Auto Join Request Bot"
BOT_VERSION = "1.0.0"

# Default approval delay (seconds)
DEFAULT_DELAY = 60

# Auto delete temporary messages (seconds)
AUTO_DELETE_TIME = 30

# Maximum channels a normal user can add
MAX_CHANNELS = 100

# ===========================
# Validation
# ===========================

required = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "MONGO_URI": MONGO_URI,
    "OWNER_ID": OWNER_ID,
}

missing = [key for key, value in required.items() if not value]

if missing:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing)}"
    )
