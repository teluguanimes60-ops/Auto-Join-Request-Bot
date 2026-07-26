from pyrogram import filters
from pyrogram.types import CallbackQuery

from loader import app


@app.on_callback_query(filters.regex("^help$"))
async def help_callback(client, query: CallbackQuery):

    await query.message.edit_text(
        "📖 Help\n\n"
        "1. Add me as admin.\n"
        "2. Enable Invite Users.\n"
        "3. Send /connect."
    )


@app.on_callback_query(filters.regex("^about$"))
async def about_callback(client, query: CallbackQuery):

    await query.message.edit_text(
        "🤖 Auto Join Request Bot\n\n"
        "Version 1.0\n"
        "Powered by Pyrogram."
    )
