from pyrogram import filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import OWNER_ID
from database import add_user, get_stats
from buttons import start_buttons, back_button, owner_buttons


HELP_TEXT = """
❓ **How to use**

1. Add this bot as an **Admin** in your channel.

2. Give it these permissions:
• Manage Chat
• Invite Users
• Manage Join Requests

3. Press **➕ Add Channel**.

4. Forward any message from your channel to this bot.

5. Configure the delay and welcome message.

The bot will automatically approve join requests after the selected delay.
"""

ABOUT_TEXT = """
🤖 **Auto Join Request Bot**

Version: 1.0

Features:

✅ Auto Accept Join Requests
✅ Custom Delay
✅ Welcome Message
✅ Multiple Channels
✅ Owner Panel
✅ Broadcast
✅ Statistics

Made with Pyrogram & MongoDB.
"""


def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


async def start_command(client, message: Message):
    """ /start """

    await add_user(message.from_user)

    text = (
        f"👋 Hello {message.from_user.mention}\n\n"
        "Welcome to **Auto Join Request Bot**.\n\n"
        "Use the buttons below to begin."
    )

    if is_owner(message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add Channel",
                        callback_data="add_channel",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📋 My Channels",
                        callback_data="my_channels",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👑 Owner Panel",
                        callback_data="owner_panel",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ℹ️ About",
                        callback_data="about",
                    ),
                    InlineKeyboardButton(
                        "❓ Help",
                        callback_data="help",
                    ),
                ],
            ]
        )
    else:
        keyboard = start_buttons()

    await message.reply_text(
        text,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


async def callback_handler(client, callback: CallbackQuery):

    data = callback.data

    await callback.answer()

    if data == "start":

        if is_owner(callback.from_user.id):

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "➕ Add Channel",
                            callback_data="add_channel",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "📋 My Channels",
                            callback_data="my_channels",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "👑 Owner Panel",
                            callback_data="owner_panel",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "ℹ️ About",
                            callback_data="about",
                        ),
                        InlineKeyboardButton(
                            "❓ Help",
                            callback_data="help",
                        ),
                    ],
                ]
            )

        else:

            keyboard = start_buttons()

        await callback.message.edit_text(
            "🏠 **Main Menu**",
            reply_markup=keyboard,
        )

        return

    if data == "help":

        await callback.message.edit_text(
            HELP_TEXT,
            reply_markup=back_button(),
        )

        return

    if data == "about":

        await callback.message.edit_text(
            ABOUT_TEXT,
            reply_markup=back_button(),
        )

        return

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

        await callback.message.edit_text(
            text,
            reply_markup=owner_buttons(),
        )

        return

    if data == "close":

        try:
            await callback.message.delete()
        except Exception:
            pass


def register(app):

    app.on_message(filters.private & filters.command("start"))(start_command)

    app.on_callback_query()(callback_handler)
