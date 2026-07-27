from pyrogram import Client, filters
from pyrogram.types import Message

from database.models import (
    get_channel,
    update_channel_setting,
)

# ==========================================================
# Waiting Users
# ==========================================================

WAITING = {}


# ==========================================================
# Ask for Welcome Message
# ==========================================================

@Client.on_callback_query(filters.regex(r"^custom_welcome_"))
async def custom_welcome(client, query):

    channel_id = int(query.data.split("_")[-1])

    WAITING[query.from_user.id] = channel_id

    await query.message.edit_text(
        "💬 **Send your custom welcome message.**\n\n"
        "Available variables:\n\n"
        "• {mention}\n"
        "• {first_name}\n"
        "• {last_name}\n"
        "• {username}\n"
        "• {channel}\n\n"
        "Send /cancel to cancel."
    )


# ==========================================================
# Save Welcome Message
# ==========================================================

@Client.on_message(filters.private & filters.text)
async def save_welcome(client, message: Message):

    user_id = message.from_user.id

    if user_id not in WAITING:
        return

    if message.text == "/cancel":

        WAITING.pop(user_id)

        return await message.reply_text(
            "❌ Cancelled."
        )

    channel_id = WAITING.pop(user_id)

    channel = await get_channel(channel_id)

    if not channel:

        return await message.reply_text(
            "Channel not found."
        )

    await update_channel_setting(
        channel_id,
        "welcome_text",
        message.text
    )

    await message.reply_text(
        "✅ Custom welcome message saved successfully."
    )
