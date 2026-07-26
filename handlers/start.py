from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from loader import app


@app.on_message(filters.private & filters.command("start"))
async def start_command(client, message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Me To Channel",
                    url="https://t.me/YourBot?startchannel"
                )
            ],
            [
                InlineKeyboardButton(
                    "📖 Help",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    "ℹ️ About",
                    callback_data="about"
                )
            ]
        ]
    )

    await message.reply_text(
        f"""👋 Hello {message.from_user.mention}!

Welcome to **Auto Join Request Bot**.

I can automatically approve join requests.

Choose an option below.""",
        reply_markup=buttons
    )
