from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from database import channels


@Client.on_message(filters.new_chat_members)
async def bot_added(client: Client, message: Message):

    me = await client.get_me()

    for member in message.new_chat_members:

        if member.id != me.id:
            continue

        chat = message.chat

        await channels.update_one(
            {"chat_id": chat.id},
            {
                "$set": {
                    "chat_id": chat.id,
                    "title": chat.title,
                    "username": chat.username,
                    "type": str(chat.type),
                    "updated_at": datetime.utcnow()
                },
                "$setOnInsert": {
                    "created_at": datetime.utcnow(),
                    "delay": 0,
                    "auto_approve": True,
                    "welcome_enabled": True
                }
            },
            upsert=True
        )

        await message.reply_text(
            "✅ AutoJoinBot is now connected.\n\n"
            "This channel has been registered successfully."
        )
