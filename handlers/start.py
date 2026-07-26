from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)

from database import users, owners


@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, message: Message):
    user = message.from_user

    # Save or Update User
    await users.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "is_bot": user.is_bot,
                "last_seen": datetime.utcnow()
            },
            "$setOnInsert": {
                "joined_at": datetime.utcnow()
            }
        },
        upsert=True
    )

    # Check Owner
    is_owner = await owners.find_one({"user_id": user.id})

    if is_owner:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👑 Owner Panel",
                        callback_data="owner_panel"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📊 Statistics",
                        callback_data="statistics"
                    ),
                    InlineKeyboardButton(
                        "⚙ Settings",
                        callback_data="settings"
                    )
                ]
            ]
        )

        text = f"""
👋 Welcome **{user.first_name}**

You are an **Owner** of AutoJoinBot.

Use the panel below to manage the bot.
"""

    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👤 My Dashboard",
                        callback_data="user_dashboard"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ℹ About",
                        callback_data="about"
                    ),
                    InlineKeyboardButton(
                        "🆘 Support",
                        callback_data="support"
                    )
                ]
            ]
        )

        text = f"""
👋 Welcome **{user.first_name}**

This bot automatically manages Telegram join requests.

Use the buttons below.
"""

    await message.reply_text(
        text,
        reply_markup=keyboard
    )
