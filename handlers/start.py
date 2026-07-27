from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import (
    OWNER_ID,
    BOT_NAME,
)

from database.models import (
    add_user,
    is_banned,
    is_admin,
)


@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    user = message.from_user

    # Check banned user
    if await is_banned(user.id):
        return await message.reply_text(
            "🚫 You are banned from using this bot."
        )

    # Save user
    await add_user(user)

    # Check role
    if user.id == OWNER_ID:
        role = "👑 Owner"
    elif await is_admin(user.id):
        role = "🛡 Admin"
    else:
        role = "👤 User"

    text = f"""
👋 Hello {user.mention}!

Welcome to **{BOT_NAME}**

This bot automatically accepts Telegram Join Requests.

━━━━━━━━━━━━━━━━━━

🪪 Role : {role}

✨ Features

✅ Auto Accept Join Requests

✅ Multi Channel Support

✅ Welcome Messages

✅ Auto Delete Messages

✅ Channel Settings

✅ Statistics

━━━━━━━━━━━━━━━━━━

Choose an option below.
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Channel",
                    callback_data="add_channel",
                )
            ],
            [
                InlineKeyboardButton(
                    "📂 My Channels",
                    callback_data="my_channels",
                ),
                InlineKeyboardButton(
                    "⚙ Settings",
                    callback_data="settings",
                ),
            ],
            [
                InlineKeyboardButton(
                    "📊 Statistics",
                    callback_data="stats",
                ),
                InlineKeyboardButton(
                    "ℹ Help",
                    callback_data="help",
                ),
            ],
        ]
    )

    # Owner Panel
    if user.id == OWNER_ID:
        buttons.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    "👑 Owner Panel",
                    callback_data="owner_panel",
                )
            ]
        )

    # Admin Panel
    elif await is_admin(user.id):
        buttons.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    "🛡 Admin Panel",
                    callback_data="admin_panel",
                )
            ]
        )

    await message.reply_text(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True,
    )
