from datetime import datetime

from pyrogram import Client
from pyrogram.types import CallbackQuery

from database import (
    users,
    owners,
    channels,
    join_requests
)

from utils.permissions import is_owner
from utils.keyboards import back_button


@Client.on_callback_query()
async def statistics_callback(client: Client, callback: CallbackQuery):

    if callback.data != "stats":
        return

    if not await is_owner(callback.from_user.id):
        return await callback.answer(
            "❌ You are not authorized.",
            show_alert=True
        )

    total_users = await users.count_documents({})
    total_owners = await owners.count_documents({})
    total_channels = await channels.count_documents({})
    total_requests = await join_requests.count_documents({})
    approved = await join_requests.count_documents(
        {"status": "approved"}
    )
    pending = await join_requests.count_documents(
        {"status": "pending"}
    )

    text = f"""
📊 **AutoJoinBot Statistics**

━━━━━━━━━━━━━━━━━━

👥 Users
• Total : `{total_users}`

👑 Owners
• Total : `{total_owners}`

📢 Channels
• Connected : `{total_channels}`

📥 Join Requests
• Total : `{total_requests}`
• Approved : `{approved}`
• Pending : `{pending}`

🕒 Server Time

`{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC`

━━━━━━━━━━━━━━━━━━

🤖 AutoJoinBot v1.0
"""

    await callback.message.edit_text(
        text,
        reply_markup=back_button("owner_panel")
    )
