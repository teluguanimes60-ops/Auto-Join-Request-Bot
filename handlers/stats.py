from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
)

from config import OWNER_ID
from database.models import (
    get_stats,
    is_admin,
)


# ==========================================================
# /stats Command
# ==========================================================

@Client.on_message(filters.private & filters.command("stats"))
async def stats_command(client: Client, message: Message):

    if (
        message.from_user.id != OWNER_ID
        and not await is_admin(message.from_user.id)
    ):
        return

    stats = await get_stats()

    text = f"""
📊 **Bot Statistics**

👥 Users : {stats['users']}

📢 Channels : {stats['channels']}

🛡 Admins : {stats['admins']}

✅ Accepted Joins : {stats['joins']}
"""

    await message.reply_text(text)


# ==========================================================
# Statistics Button
# ==========================================================

@Client.on_callback_query(filters.regex("^stats$"))
async def stats_callback(client: Client, query: CallbackQuery):

    if (
        query.from_user.id != OWNER_ID
        and not await is_admin(query.from_user.id)
    ):
        return await query.answer(
            "Access Denied",
            show_alert=True
        )

    stats = await get_stats()

    text = f"""
📊 **Bot Statistics**

👥 Users : {stats['users']}

📢 Channels : {stats['channels']}

🛡 Admins : {stats['admins']}

✅ Accepted Joins : {stats['joins']}
"""

    await query.message.edit_text(text)
