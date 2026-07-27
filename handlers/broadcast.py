from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID
from database.mongo import users

# ==========================================
# Waiting For Broadcast
# ==========================================

WAITING = set()


# ==========================================
# Broadcast Command
# ==========================================

@Client.on_message(filters.private & filters.command("broadcast"))
async def broadcast_cmd(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    WAITING.add(message.from_user.id)

    await message.reply_text(
        "📢 Send the message you want to broadcast.\n\n"
        "It can be:\n"
        "• Text\n"
        "• Photo\n"
        "• Video\n"
        "• Document\n"
        "• Sticker\n\n"
        "Send /cancel to cancel."
    )


# ==========================================
# Receive Broadcast
# ==========================================

@Client.on_message(filters.private)
async def send_broadcast(client: Client, message: Message):

    user_id = message.from_user.id

    if user_id not in WAITING:
        return

    if message.text == "/cancel":
        WAITING.remove(user_id)

        return await message.reply_text(
            "❌ Broadcast cancelled."
        )

    WAITING.remove(user_id)

    sent = 0
    failed = 0

    async for user in users.find({}):

        try:
            await message.copy(user["user_id"])
            sent += 1

        except Exception:
            failed += 1

    await message.reply_text(
        f"✅ Broadcast Completed\n\n"
        f"📤 Sent : {sent}\n"
        f"❌ Failed : {failed}"
    )
