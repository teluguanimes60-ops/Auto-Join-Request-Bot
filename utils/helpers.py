import asyncio
import logging
from datetime import datetime, timedelta

from pyrogram.errors import (
    FloodWait,
    MessageNotModified,
    RPCError,
)

logger = logging.getLogger(__name__)


# ==========================================
# Human Readable Time
# ==========================================

def format_time(seconds: int) -> str:
    if seconds <= 0:
        return "0s"

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = []

    if days:
        parts.append(f"{days}d")

    if hours:
        parts.append(f"{hours}h")

    if minutes:
        parts.append(f"{minutes}m")

    if seconds:
        parts.append(f"{seconds}s")

    return " ".join(parts)


# ==========================================
# Mention User
# ==========================================

def mention(user):
    if user.username:
        return f"@{user.username}"

    return user.mention


# ==========================================
# Progress Bar
# ==========================================

def progress_bar(current: int, total: int, length: int = 10):

    if total == 0:
        return "□□□□□□□□□□"

    percent = current / total

    filled = int(length * percent)

    return (
        "■" * filled +
        "□" * (length - filled)
    )


# ==========================================
# Percentage
# ==========================================

def percentage(current, total):

    if total == 0:
        return 0

    return round(current * 100 / total, 2)


# ==========================================
# Byte Formatter
# ==========================================

def human_bytes(size):

    power = 1024

    n = 0

    units = ["B", "KB", "MB", "GB", "TB"]

    while size >= power and n < len(units) - 1:

        size /= power

        n += 1

    return f"{size:.2f} {units[n]}"


# ==========================================
# Safe Edit
# ==========================================

async def safe_edit(message, text, **kwargs):

    try:

        await message.edit_text(
            text,
            **kwargs
        )

    except MessageNotModified:
        pass

    except RPCError as e:
        logger.error(e)


# ==========================================
# Safe Reply
# ==========================================

async def safe_reply(message, text, **kwargs):

    try:

        return await message.reply_text(
            text,
            **kwargs
        )

    except RPCError as e:

        logger.error(e)

        return None


# ==========================================
# FloodWait Handler
# ==========================================

async def run_with_floodwait(func, *args, **kwargs):

    while True:

        try:

            return await func(
                *args,
                **kwargs
            )

        except FloodWait as e:

            logger.warning(
                f"FloodWait {e.value}s"
            )

            await asyncio.sleep(
                e.value + 1
            )


# ==========================================
# Delete After
# ==========================================

async def delete_after(message, seconds=30):

    await asyncio.sleep(seconds)

    try:

        await message.delete()

    except Exception:
        pass


# ==========================================
# Current UTC Time
# ==========================================

def utc_now():

    return datetime.utcnow()


# ==========================================
# Future Time
# ==========================================

def after_seconds(seconds):

    return utc_now() + timedelta(
        seconds=seconds
    )


# ==========================================
# Validate Channel Username
# ==========================================

def valid_username(username):

    if not username:
        return False

    if username.startswith("@"):
        username = username[1:]

    return username.replace("_", "").isalnum()


# ==========================================
# Callback Data Builder
# ==========================================

def cb(action, value):

    return f"{action}:{value}"


# ==========================================
# Parse Callback Data
# ==========================================

def parse_cb(data):

    if ":" not in data:
        return data, None

    return data.split(":", 1)


# ==========================================
# Escape Markdown
# ==========================================

def escape_markdown(text):

    chars = "_*[]()~`>#+-=|{}.!\\"

    for c in chars:
        text = text.replace(c, "\\" + c)

    return text


# ==========================================
# Logger
# ==========================================

def log(text):

    logger.info(text)
