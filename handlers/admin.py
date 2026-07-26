from pyrogram import Client, filters
from pyrogram.types import Message

from database import owners


async def is_owner(user_id: int) -> bool:
    owner = await owners.find_one({"user_id": user_id})
    return owner is not None


@Client.on_message(filters.private & filters.command("panel"))
async def owner_panel(client: Client, message: Message):

    if not await is_owner(message.from_user.id):
        return await message.reply_text(
            "❌ You are not authorized to use this command."
        )

    text = f"""
👑 **AutoJoinBot Owner Panel**

Welcome, **{message.from_user.first_name}**.

━━━━━━━━━━━━━━━━━━

🤖 Bot Status : Online
👤 Your Role : Owner

━━━━━━━━━━━━━━━━━━

Available Features

• 👥 Manage Owners
• 📢 Manage Channels
• ⚙ Bot Settings
• 📊 Statistics
• 📣 Broadcast
• 📝 Logs
• 💾 Backup & Restore
• 🔄 Restart
• ❤️ Health Status

Use the dashboard buttons to manage everything.
"""

    await message.reply_text(text)
