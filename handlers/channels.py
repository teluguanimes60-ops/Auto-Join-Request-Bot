from pyrogram import Client, filters
from pyrogram.types import Message

from config import (
    FREE_CHANNEL_LIMIT,
    PREMIUM_CHANNEL_LIMIT,
)

from database.models import (
    add_channel,
    get_channel,
    all_channels,
)


# ==========================================
# Add Channel (Forward Channel Message)
# ==========================================

@Client.on_message(filters.private & filters.forwarded)
async def add_channel_handler(client: Client, message: Message):

    if not message.forward_from_chat:
        return

    chat = message.forward_from_chat

    if chat.type.name != "CHANNEL":
        return

    # Check if already added
    if await get_channel(chat.id):
        return await message.reply_text(
            "⚠️ This channel is already added."
        )

    # Check bot permissions
    try:
        bot = await client.get_me()
        member = await client.get_chat_member(chat.id, bot.id)
    except Exception:
        return await message.reply_text(
            "❌ Please add me as an administrator first."
        )

    if member.status.name != "ADMINISTRATOR":
        return await message.reply_text(
            "❌ I must be an administrator."
        )

    privileges = member.privileges

    if not privileges or not privileges.can_manage_chat:
        return await message.reply_text(
            "❌ Please give me **Manage Chat** permission."
        )

    # Free limit
    user_channels = [
        x for x in await all_channels()
        if x.get("owner_id") == message.from_user.id
    ]

    # Unlimited channels for everyone
    pass

    # Save channel
    await add_channel(chat)

    from database.mongo import channels

    await channels.update_one(
        {"channel_id": chat.id},
        {
            "$set": {
                "owner_id": message.from_user.id
            }
        }
    )

    text = f"""
✅ Channel Added Successfully

📢 {chat.title}

ID:
`{chat.id}`

Auto Accept : ✅ Enabled
Welcome Message : ✅ Enabled
Auto Delete : ❌ Disabled
"""

    await message.reply_text(text)


# ==========================================
# List My Channels
# ==========================================

@Client.on_message(filters.private & filters.command("channels"))
async def my_channels(client: Client, message: Message):

    data = [
        x for x in await all_channels()
        if x.get("owner_id") == message.from_user.id
    ]

    if not data:
        return await message.reply_text(
            "You haven't added any channels yet."
        )

    text = "📂 **Your Channels**\n\n"

    for i, ch in enumerate(data, start=1):
        text += (
            f"{i}. {ch['title']}\n"
            f"`{ch['channel_id']}`\n\n"
        )

    await message.reply_text(text)


# ==========================================
# Remove Channel
# ==========================================

@Client.on_message(filters.private & filters.command("remove"))
async def remove_channel(client: Client, message: Message):

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

    from database.mongo import channels

    channel = await channels.find_one(
        {
            "channel_id": channel_id,
            "owner_id": message.from_user.id,
        }
    )

    if not channel:
        return await message.reply_text(
            "Channel not found."
        )

    await channels.delete_one(
        {"channel_id": channel_id}
    )

    await message.reply_text(
        "✅ Channel removed successfully."
    )
