from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import users, owners, channels, join_requests
from utils.permissions import is_owner
from utils.keyboards import owner_dashboard, user_dashboard


@Client.on_callback_query()
async def callback_handler(client: Client, callback: CallbackQuery):

    data = callback.data
    user = callback.from_user

    # Close
    if data == "close":
        return await callback.message.delete()

    # ---------------- USER ---------------- #

    elif data == "user_dashboard":
        return await callback.message.edit_text(
            f"👋 Welcome {user.first_name}",
            reply_markup=user_dashboard()
        )

    elif data == "profile":

        text = f"""
👤 Profile

Name : {user.first_name}

ID : `{user.id}`

Username : @{user.username or 'None'}
"""

        return await callback.message.edit_text(
            text,
            reply_markup=user_dashboard()
        )

    elif data == "about":

        return await callback.answer(
            "AutoJoinBot Version 1.0",
            show_alert=True
        )

    elif data == "support":

        return await callback.answer(
            "Support Coming Soon.",
            show_alert=True
        )

    # ---------------- OWNER ---------------- #

    elif data == "owner_panel":

        if not await is_owner(user.id):
            return await callback.answer(
                "Access Denied",
                show_alert=True
            )

        return await callback.message.edit_text(
            "👑 Owner Dashboard",
            reply_markup=owner_dashboard()
        )

    elif data == "stats":

        if not await is_owner(user.id):
            return

        text = f"""
📊 Statistics

👥 Users : {await users.count_documents({})}

👑 Owners : {await owners.count_documents({})}

📢 Channels : {await channels.count_documents({})}

📥 Requests : {await join_requests.count_documents({})}
"""

        return await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅ Back", callback_data="owner_panel")]]
            )
        )

    elif data == "owners":

        if not await is_owner(user.id):
            return

        owner_text = ""

        async for owner in owners.find():

            owner_text += f"• `{owner['user_id']}`\n"

        if owner_text == "":
            owner_text = "No Owners"

        return await callback.message.edit_text(
            "👥 Owners\n\n" + owner_text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅ Back", callback_data="owner_panel")]]
            )
        )

    elif data == "channels":

        if not await is_owner(user.id):
            return

        text = "📢 Channel Manager\n\n"

        total = 0

        async for channel in channels.find():

            total += 1

            text += f"• {channel.get('title','Unknown')}\n"
            text += f"`{channel['chat_id']}`\n\n"

        if total == 0:
            text += "No channels connected."

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ How to Add Channel",
                        callback_data="add_channel"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="owner_panel"
                    )
                ]
            ]
        )

        return await callback.message.edit_text(
            text,
            reply_markup=keyboard
        )

    elif data == "add_channel":

        text = """
📢 Add a Channel

1️⃣ Add this bot as Admin.

2️⃣ Enable

✅ Manage Chat Join Requests

3️⃣ Send one Join Request.

The bot will automatically register the channel.
"""

        return await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅ Back", callback_data="channels")]]
            )
        )

    elif data in [
        "analytics",
        "settings",
        "welcome",
        "delay",
        "broadcast",
        "backup",
        "logs",
        "health",
        "bot_info"
    ]:

        return await callback.answer(
            "🚧 This feature will be added next.",
            show_alert=True
        )

    else:

        return await callback.answer("Unknown Button")
