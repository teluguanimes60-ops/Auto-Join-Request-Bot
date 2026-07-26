from pyrogram import Client, filters
from pyrogram.types import Message

from database import channels
from utils.permissions import is_owner


@Client.on_message(filters.private & filters.command("setdelay"))
async def set_delay(client: Client, message: Message):

    if not await is_owner(message.from_user.id):
        return await message.reply_text(
            "❌ You are not authorized."
        )

    args = message.text.split()

    if len(args) != 3:
        return await message.reply_text(
            "Usage:\n"
            "/setdelay <channel_id> <seconds>"
        )

    try:
        chat_id = int(args[1])
        delay = int(args[2])
    except ValueError:
        return await message.reply_text(
            "Invalid values."
        )

    await channels.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "delay": delay
            }
        }
    )

    await message.reply_text(
        f"✅ Delay updated to **{delay}** seconds."
    )


@Client.on_message(filters.private & filters.command("channel"))
async def channel_info(client: Client, message: Message):

    if not await is_owner(message.from_user.id):
        return

    args = message.text.split()

    if len(args) != 2:
        return await message.reply_text(
            "/channel <channel_id>"
        )

    try:
        chat_id = int(args[1])
    except ValueError:
        return await message.reply_text(
            "Invalid Channel ID."
        )

    channel = await channels.find_one(
        {"chat_id": chat_id}
    )

    if not channel:
        return await message.reply_text(
            "Channel not found."
        )

    text = (
        f"📢 **{channel.get('title')}**\n\n"
        f"🆔 `{chat_id}`\n"
        f"⏳ Delay: {channel.get('delay', 0)} sec\n"
        f"✅ Auto Approve: {channel.get('auto_approve', True)}"
    )

    await message.reply_text(text)
