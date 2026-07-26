import asyncio
import logging
from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)

from config import OWNER_ID
from database import (
    add_user,
    add_channel,
    get_channel,
    get_owner_channels,
    remove_channel,
    set_delay,
    get_delay,
    set_welcome,
    get_welcome,
    set_status,
    get_status,
    get_stats,
    all_users,
    add_log
)

from buttons import (
    start_buttons,
    back_button,
    channel_settings,
    delay_buttons,
    owner_buttons,
    confirm_remove,
    close_button
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# Runtime Memory
# ==========================================================

# Used for temporary user actions.
# Example:
# waiting_forward
# waiting_welcome
# waiting_delay

USER_STATE = {}

# Store scheduled approval tasks
JOIN_TASKS = {}

# Messages that should be auto-deleted
DELETE_QUEUE = {}


# ==========================================================
# User State
# ==========================================================

def set_state(user_id: int, state: str, value=None):
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {}

    USER_STATE[user_id][state] = value


def get_state(user_id: int, state: str):
    return USER_STATE.get(user_id, {}).get(state)


def clear_state(user_id: int):
    USER_STATE.pop(user_id, None)


# ==========================================================
# Auto Delete Messages
# ==========================================================

async def auto_delete(message: Message, seconds: int = 20):
    try:
        await asyncio.sleep(seconds)
        await message.delete()
    except Exception:
        pass


async def safe_reply(
    message: Message,
    text: str,
    reply_markup=None
):
    msg = await message.reply_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    asyncio.create_task(
        auto_delete(msg)
    )

    return msg


# ==========================================================
# Safe Edit
# ==========================================================

async def safe_edit(
    message: Message,
    text: str,
    reply_markup=None
):
    try:
        await message.edit_text(
            text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception:
        pass


# ==========================================================
# Permission Check
# ==========================================================

async def bot_can_manage(client, channel_id):

    try:
        me = await client.get_chat_member(
            channel_id,
            "me"
        )

        if me.status != ChatMemberStatus.ADMINISTRATOR:
            return False

        if not me.privileges:
            return False

        return bool(
            me.privileges.can_manage_chat
            or me.privileges.can_invite_users
        )

    except Exception:
        return False


# ==========================================================
# Format Time
# ==========================================================

def format_delay(seconds: int):

    if seconds < 60:
        return f"{seconds} Seconds"

    if seconds < 3600:
        return f"{seconds // 60} Minutes"

    return f"{seconds // 3600} Hours"


# ==========================================================
# Owner Check
# ==========================================================

def is_owner(user_id: int):
    return user_id == OWNER_ID


# ==========================================================
# Logger
# ==========================================================

async def save_log(text):

    logger.info(text)

    try:
        await add_log(
            f"[{datetime.now()}] {text}"
        )
    except Exception:
        pass
# ==========================================================
# START COMMAND
# ==========================================================

async def start_command(client, message: Message):
    user = message.from_user

    await add_user(user)

    text = f"""
👋 Hello {user.mention}!

Welcome to **Auto Join Request Bot**

I can automatically approve join requests after the delay you choose.

Click **Add Channel** to begin.
"""

    if is_owner(user.id):
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")
            ],
            [
                InlineKeyboardButton("📋 My Channels", callback_data="my_channels")
            ],
            [
                InlineKeyboardButton("👑 Owner Panel", callback_data="owner_panel")
            ],
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
# HELP
# ==========================================================

HELP_TEXT = """
❓ **How to use**

1. Add this bot as an Admin in your channel.

2. Enable:
• Manage Chat
• Invite Users
• Manage Join Requests

3. Press **Add Channel**.

4. Forward any message from your channel.

5. Choose a delay.

Now every join request will be accepted automatically after the selected time.
"""


# ==========================================================
# ABOUT
# ==========================================================

ABOUT_TEXT = """
🤖 **Auto Join Request Bot**

Version: 1.0

Features:

✅ Auto Join Request Approval
✅ Custom Delay
✅ Welcome Message
✅ Multiple Channels
✅ Owner Panel
✅ Broadcast
✅ Statistics

Powered by Pyrogram & MongoDB
"""


# ==========================================================
# CALLBACK HANDLER
# ==========================================================

async def callback_handler(client, callback: CallbackQuery):

    data = callback.data

    try:
        await callback.answer()
    except Exception:
        pass

    # ---------------- Start ----------------

    if data == "start":

        if is_owner(callback.from_user.id):

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "➕ Add Channel",
                        callback_data="add_channel"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📋 My Channels",
                        callback_data="my_channels"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👑 Owner Panel",
                        callback_data="owner_panel"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ℹ️ About",
                        callback_data="about"
                    ),
                    InlineKeyboardButton(
                        "❓ Help",
                        callback_data="help"
                    )
                ]
            ])

        else:

            keyboard = start_buttons()

        await safe_edit(
            callback.message,
            "🏠 **Main Menu**",
            keyboard
        )

        return

    # ---------------- Help ----------------

    if data == "help":

        await safe_edit(
            callback.message,
            HELP_TEXT,
            back_button()
        )

        return

    # ---------------- About ----------------

    if data == "about":

        await safe_edit(
            callback.message,
            ABOUT_TEXT,
            back_button()
        )

        return

    # ---------------- Owner Panel ----------------

    if data == "owner_panel":

        if not is_owner(callback.from_user.id):
            return

        stats = await get_stats()

        text = (
            "👑 **Owner Panel**\n\n"
            f"👥 Users : {stats['users']}\n"
            f"📺 Channels : {stats['channels']}\n"
            f"📜 Logs : {stats['logs']}"
        )

        await safe_edit(
            callback.message,
            text,
            owner_buttons()
        )

        return

    # ---------------- Close ----------------

    if data == "close":

        try:
            await callback.message.delete()
        except Exception:
            pass

        return


  
