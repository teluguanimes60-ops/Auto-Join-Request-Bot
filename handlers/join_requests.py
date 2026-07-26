import asyncio
from datetime import datetime

from pyrogram import Client
from pyrogram.handlers import ChatJoinRequestHandler
from pyrogram.types import ChatJoinRequest

from database import channels, join_requests


async def handle_join_request(client: Client, request: ChatJoinRequest):
    chat = request.chat
    user = request.from_user

    # Get channel settings
    channel = await channels.find_one(
        {"chat_id": chat.id}
    )

    # If channel isn't registered, approve immediately
    if not channel:
        await request.approve()
        return

    # Get delay (seconds)
    delay = int(channel.get("delay", 0))

    if delay > 0:
        await asyncio.sleep(delay)

    # Approve request
    await request.approve()

    # Save request
    await join_requests.update_one(
        {
            "chat_id": chat.id,
            "user_id": user.id
        },
        {
            "$set": {
                "chat_title": chat.title,
                "username": user.username,
                "first_name": user.first_name,
                "approved": True,
                "approved_at": datetime.utcnow()
            },
            "$setOnInsert": {
                "requested_at": datetime.utcnow()
            }
        },
        upsert=True
    )

    print(
        f"Approved {user.id} -> {chat.title}"
    )


app = Client.get_instance()

app.add_handler(
    ChatJoinRequestHandler(handle_join_request)
)
