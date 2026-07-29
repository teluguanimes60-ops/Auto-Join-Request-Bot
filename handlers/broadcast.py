import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID
from database.mongo import users


# ==========================================================
# Waiting For Broadcast
# ==========================================================

WAITING = set()


# ==========================================================
# Broadcast Command
# ==========================================================

@Client.on_message(filters.private & filters.command("broadcast"))
async def broadcast_cmd(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    WAITING.add(message.from_user.id)

    await message.reply_text(
        "📢 **Broadcast Mode Enabled**\n\n"
        "Send any message to broadcast.\n\n"
        "Supported:\n"
        "• Text\n"
        "• Photo\n"
        "• Video\n"
        "• Document\n"
        "• Audio\n"
        "• Sticker\n"
        "• Animation\n"
        "• Voice\n\n"
        "Send /cancel to cancel."
    )


# ==========================================================
# Receive Broadcast
# ==========================================================

@Client.on_message(filters.private)
async def send_broadcast(client: Client, message: Message):

    user_id = message.from_user.id

    if user_id not in WAITING:
        return

    if message.text and message.text == "/cancel":

        WAITING.remove(user_id)

        return await message.reply_text(
            "❌ Broadcast Cancelled."
        )

    WAITING.remove(user_id)

    status = await message.reply_text(
        "📤 Starting Broadcast..."
    )

    total = await users.count_documents({})

    sent = 0
    failed = 0

    async for user in users.find({}):

        try:

            await message.copy(user["user_id"])

            sent += 1

        except Exception:

            failed += 1

        if (sent + failed) % 25 == 0:

            await status.edit_text(
                f"""
📤 Broadcasting...

👥 Total : {total}

✅ Sent : {sent}

❌ Failed : {failed}
"""
            )

        await asyncio.sleep(0.05)

    await status.edit_text(
        f"""
✅ Broadcast Completed

👥 Total Users : {total}

📤 Sent : {sent}

❌ Failed : {failed}
"""
    )
