from pyrogram import Client, filters
from pyrogram.types import Message

from database.models import (
    add_channel,
    get_channel,
)

from database.mongo import channels


# ==========================================================
# Add Channel
# ==========================================================

@Client.on_message(filters.private & filters.forwarded)
async def add_channel_handler(client: Client, message: Message):

    if not message.forward_from_chat:
        return

    chat = message.forward_from_chat

    if chat.type.name != "CHANNEL":
        return

    # Already added
    if await get_channel(chat.id):
        return await message.reply_text(
            "⚠️ This channel is already registered."
        )

    # Check bot admin
    try:
        bot = await client.get_me()
        member = await client.get_chat_member(chat.id, bot.id)
    except Exception:
        return await message.reply_text(
            "❌ Add me as an administrator first."
        )

    if member.status.name != "ADMINISTRATOR":
        return await message.reply_text(
            "❌ I must be an administrator."
        )

    if (
        not member.privileges
        or not member.privileges.can_manage_chat
    ):
        return await message.reply_text(
            "❌ Please give me Manage Chat permission."
        )

    # Save channel
    await add_channel(chat, owner_id=message.from_user.id)

    await message.reply_text(
        f"""
✅ Channel Added Successfully

📢 **{chat.title}**

🆔 `{chat.id}`

━━━━━━━━━━━━━━━━━━

✅ Auto Accept : Enabled

✅ Welcome Message : Enabled

❌ Auto Delete : Disabled

🚫 Force Subscribe : Disabled

━━━━━━━━━━━━━━━━━━

Use /channels to manage your channels.
"""
    )


# ==========================================================
# My Channels
# ==========================================================

@Client.on_message(filters.private & filters.command("channels"))
async def my_channels(client: Client, message: Message):

    data = await channels.find(
        {
            "owner_id": message.from_user.id
        }
    ).to_list(length=None)

    if not data:
        return await message.reply_text(
            "❌ You haven't added any channels."
        )

    text = "📂 **Your Channels**\n\n"

    for i, ch in enumerate(data, start=1):

        text += (
            f"{i}. {ch['title']}\n"
            f"🆔 `{ch['channel_id']}`\n"
        )

        if ch.get("force_sub"):
            text += "🚫 Force Subscribe : ON\n"
        else:
            text += "🚫 Force Subscribe : OFF\n"

        text += "\n"

    await message.reply_text(text)


# ==========================================================
# Remove Channel
# ==========================================================

@Client.on_message(filters.private & filters.command("remove"))
async def remove_channel_cmd(client: Client, message: Message):

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/remove CHANNEL_ID"
        )

    try:
        channel_id = int(message.command[1])
    except ValueError:
        return await message.reply_text(
            "Invalid Channel ID."
        )

    channel = await channels.find_one(
        {
            "channel_id": channel_id,
            "owner_id": message.from_user.id,
        }
    )

    if not channel:
        return await message.reply_text(
            "❌ Channel not found."
        )

    await channels.delete_one(
        {
            "channel_id": channel_id
        }
    )

    await message.reply_text(
        "✅ Channel removed successfully."
    )
