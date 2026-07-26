import asyncio
from datetime import datetime

from pyrogram import Client
from pyrogram.types import ChatJoinRequest

from database import channels, join_requests


@Client.on_chat_join_request()
async def join_request_handler(client: Client, request: ChatJoinRequest):
    chat = request.chat
    user = request.from_user

    # Get channel settings
    channel = await channels.find_one(
        {"chat_id": chat.id}
    )

    # Default settings
    delay = 0
    auto_approve = True

    if channel:
        delay = int(channel.get("delay", 0))
        auto_approve = channel.get("auto_approve", True)

    # Save request
    await join_requests.update_one(
        {
            "chat_id": chat.id,
            "user_id": user.id
        },
        {
            "$set": {
                "chat_title": chat.title,
                "chat_username": chat.username,
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "status": "pending",
                "requested_at": datetime.utcnow()
            }
        },
        upsert=True
    )

    if not auto_approve:
        return

    if delay > 0:
        await asyncio.sleep(delay)

    # Approve request
    await request.approve()

    # Update status
    await join_requests.update_one(
        {
            "chat_id": chat.id,
            "user_id": user.id
        },
        {
            "$set": {
                "status": "approved",
                "approved_at": datetime.utcnow()
            }
        }
    )

    print(
        f"✅ Approved {user.first_name} ({user.id}) -> {chat.title}"
    )
