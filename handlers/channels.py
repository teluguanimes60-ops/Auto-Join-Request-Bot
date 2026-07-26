from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from database import channels


@Client.on_message(filters.new_chat_members)
async def bot_added(client: Client, message: Message):
    """
    Save a channel/group when this bot is added as an administrator.
    """

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
                    "type": chat.type.value,
                    "updated_at": datetime.utcnow()
                },
                "$setOnInsert": {
                    "created_at": datetime.utcnow(),
                    "delay": 0,
                    "auto_approve": True,
                    "welcome_enabled": True,
                    "welcome_text": (
                        "👋 Welcome to {chat_name}!\n\n"
                        "Enjoy your stay."
                    ),
                    "owners": [],
                    "logs": None,
                    "force_join": [],
                    "buttons": []
                }
            },
            upsert=True
        )

        await message.reply_text(
            "✅ **AutoJoinBot** has been added successfully.\n\n"
            "This channel has been registered.\n"
            "Use **/panel** in my private chat to manage its settings."
        )
