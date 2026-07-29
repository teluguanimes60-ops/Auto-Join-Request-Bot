from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import OWNER_ID
from database.models import (
    get_stats,
    is_admin,
)


# ==========================================================
# Statistics Text
# ==========================================================

async def build_stats():

    stats = await get_stats()

    return f"""
📊 **Bot Statistics**

━━━━━━━━━━━━━━━━━━

👥 Users          : {stats['users']}

📢 Channels       : {stats['channels']}

🛡 Admins         : {stats['admins']}

✅ Accepted Joins : {stats['joins']}

━━━━━━━━━━━━━━━━━━

🤖 Auto Join Request Bot
"""


# ==========================================================
# /stats
# ==========================================================

@Client.on_message(filters.private & filters.command("stats"))
async def stats_command(client: Client, message: Message):

    if (
        message.from_user.id != OWNER_ID
        and not await is_admin(message.from_user.id)
    ):
        return

    await message.reply_text(
        await build_stats(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔄 Refresh",
                        callback_data="stats"
                    )
                ]
            ]
        )
    )


# ==========================================================
# Callback
# ==========================================================

@Client.on_callback_query(filters.regex("^stats$"))
async def stats_callback(client: Client, query: CallbackQuery):

    if (
        query.from_user.id != OWNER_ID
        and not await is_admin(query.from_user.id)
    ):
        return await query.answer(
            "❌ Access Denied",
            show_alert=True
        )

    await query.message.edit_text(
        await build_stats(),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔄 Refresh",
                        callback_data="stats"
                    ),
                    InlineKeyboardButton(
                        "🏠 Home",
                        callback_data="home"
                    )
                ]
            ]
        )
    )

    await query.answer("Updated")
