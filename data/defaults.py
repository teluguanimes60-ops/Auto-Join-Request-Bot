"""
AutoJoinBot Default Configuration
"""

BOT_NAME = "AutoJoinBot"
BOT_VERSION = "1.0.0"

# ------------------------
# Channel Defaults
# ------------------------

DEFAULT_CHANNEL = {
    "delay": 0,
    "auto_approve": True,
    "welcome_enabled": False,
    "title": "",
    "username": "",
    "type": "",
    "created_at": None,
    "updated_at": None,
}

# ------------------------
# Join Request Defaults
# ------------------------

DEFAULT_JOIN_REQUEST = {
    "status": "pending",
    "approved": False,
    "requested_at": None,
    "approved_at": None,
    "error": None,
}

# ------------------------
# User Defaults
# ------------------------

DEFAULT_USER = {
    "is_owner": False,
    "language": "en",
    "created_at": None,
}

# ------------------------
# Bot Settings
# ------------------------

DEFAULT_SETTINGS = {
    "maintenance": False,
    "statistics": True,
    "save_history": True,
}
