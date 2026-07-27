from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


@Client.on_callback_query()
async def about_callback(client: Client, query: CallbackQuery):

    if query.data != "about":
        return

    text = """
🤖 **Auto Join Request Bot**

Automatically accepts Telegram Channel Join Requests.

✨ Features

✅ Unlimited Channels
✅ Auto Accept Join Requests
✅ Welcome Messages
✅ Auto Delete Welcome Messages
✅ Per Channel Settings
✅ Owner Panel
✅ Admin Panel
✅ Statistics
✅ Broadcast
✅ MongoDB Database
✅ GitHub + Render Support

👨‍💻 Version : 1.0

Made with ❤️ using Pyrogram.
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❓ Help",
                    callback_data="help"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ]
    )

    await query.message.edit_text(
        text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
