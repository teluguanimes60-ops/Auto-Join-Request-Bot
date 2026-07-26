import asyncio
import logging
from datetime import datetime

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import OWNER_ID
from database import (
    add_user,
    get_stats,
    add_log
)
from buttons import (
    start_buttons,
    back_button,
    owner_buttons
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# Runtime Memory
# ==========================================================

USER_STATE = {}

# ==========================================================
# User State Helpers
# ==========================================================

def set_state(user_id: int, key: str, value):
    USER_STATE.setdefault(user_id, {})
    USER_STATE[user_id][key] = value


def get_state(user_id: int, key: str):
    return USER_STATE.get(user_id, {}).get(key)


def clear_state(user_id: int):
    USER_STATE.pop(user_id, None)


# ==========================================================
# Helpers
# ==========================================================

def is_owner(user_id: int):
    return user_id == OWNER_ID


async def safe_edit(message: Message, text: str, reply_markup=None):
    try:
        await message.edit_text(
            text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception:
        pass


async def save_log(text: str):
    logger.info(text)
    try:
        await add_log(f"[{datetime.now()}] {text}")
    except Exception:
        pass


# ==========================================================
# Start Command
# ==========================================================

async def start_command(client: Client, message: Message):
    await add_user(message.from_user)

    text = (
        f"👋 Hello {message.from_user.mention}!\n\n"
        "Welcome to **Auto Join Request Bot**.\n\n"
        "I can automatically approve channel join requests "
        "after the delay you configure."
    )

    if is_owner(message.from_user.id):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")],
            [InlineKeyboardButton("📋 My Channels", callback_data="my_channels")],
            [InlineKeyboardButton("👑 Owner Panel", callback_data="owner_panel")],
            [
                InlineKeyboardButton("ℹ️ About", callback_data="about"),
                InlineKeyboardButton("❓ Help", callback_data="help")
            ]
        ])
    else:
        keyboard = start_buttons()

    await message.reply_text(
        text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


# ==========================================================
# Help & About
# ==========================================================

HELP_TEXT = """
❓ How to use

1. Add this bot as Admin in your channel.
2. Give it:
   • Manage Chat
   • Invite Users
   • Manage Join Requests
3. Click Add Channel.
4. Forward a message from your channel.
5. Set the approval delay.

Done! Join requests will be approved automatically.
"""

ABOUT_TEXT = """
🤖 Auto Join Request Bot

Version: 1.0

Features:
• Auto Join Request Approval
• Custom Delay
• Welcome Message
• Multiple Channels
• Owner Panel
• Broadcast
• Statistics
"""


# ==========================================================
# Callback Handler (Basic)
# ==========================================================

async def callback_handler(client: Client, callback: CallbackQuery):

    data = callback.data

    await callback.answer()

    if data == "start":

        if is_owner(callback.from_user.id):
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")],
                [InlineKeyboardButton("📋 My Channels", callback_data="my_channels")],
                [InlineKeyboardButton("👑 Owner Panel", callback_data="owner_panel")],
                [
                    InlineKeyboardButton("ℹ️ About", callback_data="about"),
                    InlineKeyboardButton("❓ Help", callback_data="help")
                ]
            ])
        else:
            keyboard = start_buttons()

        await safe_edit(callback.message, "🏠 Main Menu", keyboard)
        return

    if data == "help":
        await safe_edit(callback.message, HELP_TEXT, back_button())
        return

    if data == "about":
        await safe_edit(callback.message, ABOUT_TEXT, back_button())
        return

    if data == "owner_panel":

        if not is_owner(callback.from_user.id):
            return

        stats = await get_stats()

        text = (
            "👑 Owner Panel\n\n"
            f"👥 Users: {stats['users']}\n"
            f"📺 Channels: {stats['channels']}\n"
            f"📜 Logs: {stats['logs']}"
        )

        await safe_edit(
            callback.message,
            text,
            owner_buttons()
        )
        return

    if data == "close":
        try:
            await callback.message.delete()
        except Exception:
            pass

