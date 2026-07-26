from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from database import users, owners
from utils.keyboards import owner_dashboard, user_dashboard


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

    # Check if user is an Owner
    is_owner = await owners.find_one({"user_id": user.id})

    if is_owner:
        text = f"""
👋 Hello, **{user.first_name}**!

Welcome to **AutoJoinBot**.

You are an **Owner** of this bot.

Use the dashboard below to manage everything.
"""

        await message.reply_text(
            text=text,
            reply_markup=owner_dashboard()
        )

    else:
        text = f"""
👋 Hello, **{user.first_name}**!

Welcome to **AutoJoinBot**.

This bot automatically manages Telegram join requests.

Use the dashboard below.
"""

        await message.reply_text(
            text=text,
            reply_markup=user_dashboard()
        )
