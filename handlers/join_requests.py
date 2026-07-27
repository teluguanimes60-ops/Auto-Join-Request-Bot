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
        print(f"Join Request Error : {e}")
        return

    # Save Join Log
    await log_join(channel_id, user.id)

    # Send Welcome Message
    welcome_message = None

    if channel.get("welcome", True):

        text = DEFAULT_WELCOME.format(
            mention=user.mention
        )

        try:
            welcome_message = await client.send_message(
                chat_id=channel_id,
                text=text,
            )
        except Exception:
            pass

    # Auto Delete Welcome Message
    if (
        welcome_message
        and channel.get("auto_delete", False)
    ):

        await asyncio.sleep(30)

        try:
            await welcome_message.delete()
        except Exception:
            pass

    # Log Channel
    if LOG_CHANNEL:

        try:
            await client.send_message(
                LOG_CHANNEL,
                (
                    "✅ Join Request Accepted\n\n"
                    f"👤 User : {user.mention}\n"
                    f"🆔 `{user.id}`\n\n"
                    f"📢 Channel : {join_request.chat.title}\n"
                    f"🆔 `{channel_id}`"
                ),
            )
        except Exception:
            pass
