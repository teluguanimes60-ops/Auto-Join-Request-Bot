from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import OWNER_ID, BOT_NAME

from database.models import (
    add_user,
    is_banned,
    is_admin,
)


@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message):

    print("START COMMAND RECEIVED")

    user = message.from_user

    try:

        if await is_banned(user.id):
            return await message.reply_text(
                "🚫 You are banned."
            )

        await add_user(user)

        if user.id == OWNER_ID:
            role = "👑 Owner"

        elif await is_admin(user.id):
            role = "🛡 Admin"

        else:
            role = "👤 User"

    except Exception as e:

        print("DATABASE ERROR:", e)

        role = "👤 User"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Channel",
                    callback_data="add_channel"
                )
            ]
        ]
    )

    await message.reply_text(
        f"Hello {user.mention}\n\n"
        f"Welcome to {BOT_NAME}\n\n"
        f"Role : {role}",
        reply_markup=buttons
    )
