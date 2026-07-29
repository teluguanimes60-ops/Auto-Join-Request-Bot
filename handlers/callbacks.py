from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import OWNER_ID
from database.models import is_admin


# ==========================================================
# Back to Home
# ==========================================================

@Client.on_callback_query(filters.regex("^home$"))
async def home_callback(client: Client, query: CallbackQuery):

    user = query.from_user

    if user.id == OWNER_ID:
        role = "👑 Owner"
    elif await is_admin(user.id):
        role = "🛡 Admin"
    else:
        role = "👤 User"

    text = f"""
👋 Welcome {user.mention}

━━━━━━━━━━━━━━━━━━

Role : {role}

Choose an option below.

━━━━━━━━━━━━━━━━━━
"""

    buttons = [
        [
            InlineKeyboardButton(
                "➕ Add Channel",
                callback_data="add_channel"
            )
        ],
        [
            InlineKeyboardButton(
                "📂 My Channels",
                callback_data="my_channels"
            ),
            InlineKeyboardButton(
                "⚙ Settings",
                callback_data="settings"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="stats"
            ),
            InlineKeyboardButton(
                "ℹ Help",
                callback_data="help"
            )
        ]
    ]

    if user.id == OWNER_ID:
        buttons.append(
            [
                InlineKeyboardButton(
                    "👑 Owner Panel",
                    callback_data="owner_panel"
                )
            ]
        )

    elif await is_admin(user.id):
        buttons.append(
            [
                InlineKeyboardButton(
                    "🛡 Admin Panel",
                    callback_data="admin_panel"
                )
            ]
        )

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# ==========================================================
# Help
# ==========================================================

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(client: Client, query: CallbackQuery):

    text = """
❓ **Help**

This bot automatically accepts Telegram Join Requests.

Steps:

1. Add the bot as Admin.
2. Enable Invite Requests.
3. Add your channel.
4. Done.

The bot will automatically approve users.
"""

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="home"
                    )
                ]
            ]
        )
    )


# ==========================================================
# About
# ==========================================================

@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(client: Client, query: CallbackQuery):

    text = """
🤖 **Auto Join Request Bot**

Version : 1.0

Features

✅ Auto Accept
✅ Welcome Message
✅ Auto Delete
✅ Multi Channel
✅ Statistics
✅ Admin Panel
"""

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="home"
                    )
                ]
            ]
        )
    )


# ==========================================================
# Close
# ==========================================================

@Client.on_callback_query(filters.regex("^close$"))
async def close_callback(client: Client, query: CallbackQuery):

    await query.message.delete()
