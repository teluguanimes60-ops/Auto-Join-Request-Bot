from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from buttons import start_buttons
from config import OWNER_ID
from database.models import is_admin


# ==========================================================
# HOME
# ==========================================================

@Client.on_callback_query(filters.regex("^home$|^start$"))
async def home_callback(client: Client, query: CallbackQuery):

    owner = query.from_user.id == OWNER_ID

    admin = await is_admin(query.from_user.id)

    text = f"""
👋 Welcome {query.from_user.first_name}

🤖 Auto Join Request Bot

Automatically accepts Telegram Channel Join Requests.

━━━━━━━━━━━━━━━━━━

➕ Add your channels

⚙ Configure settings

✅ Auto Accept Join Requests

💬 Welcome Messages

━━━━━━━━━━━━━━━━━━

Select an option below.
"""

    await query.message.edit_text(
        text,
        reply_markup=start_buttons(
            is_owner=owner
        )
    )
