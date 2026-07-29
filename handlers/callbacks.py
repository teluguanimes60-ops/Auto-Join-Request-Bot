from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from keyboards.buttons import (
    start_buttons,
    owner_buttons,
)

from database.models import (
    get_stats,
)

from config import OWNER_ID


# ==========================================================
# Ignore Button
# ==========================================================

@Client.on_callback_query(filters.regex("^ignore$"))
async def ignore_callback(client, query: CallbackQuery):

    await query.answer()


# ==========================================================
# Close
# ==========================================================

@Client.on_callback_query(filters.regex("^close$"))
async def close_callback(client, query: CallbackQuery):

    await query.message.delete()


# ==========================================================
# Back To Start
# ==========================================================

@Client.on_callback_query(filters.regex("^start$"))
async def back_start(client, query: CallbackQuery):

    await query.message.edit_text(
        "🏠 **Main Menu**\n\n"
        "Select an option below.",
        reply_markup=start_buttons()
    )


# ==========================================================
# About
# ==========================================================

@Client.on_callback_query(filters.regex("^about$"))
async def about_callback(client, query: CallbackQuery):

    await query.message.edit_text(
        "🤖 **Auto Join Request Bot**\n\n"
        "Automatically accepts Telegram join requests.\n\n"
        "Supports:\n"
        "• Multi Channels\n"
        "• Welcome Messages\n"
        "• Auto Delete\n"
        "• Admin Panel\n"
        "• Statistics",
        reply_markup=start_buttons()
    )


# ==========================================================
# Help
# ==========================================================

@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(client, query: CallbackQuery):

    await query.message.edit_text(
        "**How to use**\n\n"
        "1. Add the bot as Admin.\n"
        "2. Enable Join Requests.\n"
        "3. Click Add Channel.\n"
        "4. Send the Channel ID.\n"
        "5. Done.",
        reply_markup=start_buttons()
    )


# ==========================================================
# Owner Panel
# ==========================================================

@Client.on_callback_query(filters.regex("^owner_panel$"))
async def owner_panel(client, query: CallbackQuery):

    if query.from_user.id != OWNER_ID:

        return await query.answer(
            "Owner Only",
            show_alert=True
        )

    await query.message.edit_text(
        "👑 **Owner Panel**",
        reply_markup=owner_buttons()
    )


# ==========================================================
# Statistics
# ==========================================================

@Client.on_callback_query(filters.regex("^stats$"))
async def stats_callback(client, query: CallbackQuery):

    stats = await get_stats()

    text = (
        "📊 **Bot Statistics**\n\n"
        f"👥 Users : {stats['users']}\n"
        f"👮 Admins : {stats['admins']}\n"
        f"📺 Channels : {stats['channels']}\n"
        f"✅ Accepted : {stats['joins']}"
    )

    await query.message.edit_text(
        text,
        reply_markup=start_buttons()
    )
