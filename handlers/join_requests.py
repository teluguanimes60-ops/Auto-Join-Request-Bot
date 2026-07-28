import asyncio

from pyrogram import Client
from pyrogram.types import ChatJoinRequest

from config import (
    DEFAULT_WELCOME,
    LOG_CHANNEL,
)

from database.models import (
    get_channel,
    log_join,
)


# ==========================================================
# AUTO ACCEPT JOIN REQUEST
# ==========================================================

@Client.on_chat_join_request()
async def auto_accept_join_request(client: Client, join_request: ChatJoinRequest):
    """
    Automatically accepts join requests.
    """

    channel_id = join_request.chat.id
    user = join_request.from_user

    # Get channel settings
    channel = await get_channel(channel_id)

    # Channel not registered
    if not channel:
        return

    # Auto Accept disabled
    if not channel.get("auto_accept", True):
        return

    # Accept Join Request
    try:
        await join_request.approve()

    except Exception as e:
        print(f"Join Request Error: {e}")
        return

    # Save Join Log
    await log_join(channel_id, user.id)

    # Welcome Message
    welcome_message = None

    if channel.get("welcome", True):

        text = channel.get(
            "welcome_text",
            DEFAULT_WELCOME
        )

        try:
            text = text.format(
                mention=user.mention,
                first_name=user.first_name or "",
                last_name=user.last_name or "",
                username=f"@{user.username}" if user.username else "None",
                channel=join_request.chat.title,
            )
        except Exception:
            text = DEFAULT_WELCOME.format(
                mention=user.mention,
                first_name=user.first_name or "",
                last_name=user.last_name or "",
                username=f"@{user.username}" if user.username else "None",
                channel=join_request.chat.title,
            )

        try:
            welcome_message = await client.send_message(
                chat_id=channel_id,
                text=text,
            )
        except Exception as e:
            print(f"Welcome Message Error: {e}")

    # Auto Delete Welcome Message
    if welcome_message and channel.get("auto_delete", False):

        delete_time = channel.get("delete_time", 30)

        await asyncio.sleep(delete_time)

        try:
            await welcome_message.delete()
        except Exception:
            pass

    # Send Log
    if LOG_CHANNEL:

        try:
            await client.send_message(
                LOG_CHANNEL,
                (
                    "✅ **Join Request Accepted**\n\n"
                    f"👤 User: {user.mention}\n"
                    f"🆔 `{user.id}`\n\n"
                    f"📢 Channel: {join_request.chat.title}\n"
                    f"🆔 `{channel_id}`"
                ),
            )
        except Exception:
            pass
