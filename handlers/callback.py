from pyrogram import Client
from pyrogram.types import CallbackQuery

from database import users, owners, channels, join_requests
from utils.permissions import is_owner
from utils.keyboards import (
    owner_dashboard,
    user_dashboard,
    channel_panel,
    back_button
)


@Client.on_callback_query()
async def callback_handler(client: Client, callback: CallbackQuery):

    user = callback.from_user
    data = callback.data

    # ===============================
    # CLOSE
    # ===============================

    if data == "close":
        return await callback.message.delete()

    # ===============================
    # USER DASHBOARD
    # ===============================

    if data == "user_dashboard":

        return await callback.message.edit_text(
            f"👋 Hello {user.first_name}\n\n"
            "Welcome to AutoJoinBot.",
            reply_markup=user_dashboard()
        )

    # ===============================
    # PROFILE
    # ===============================

    if data == "profile":

        text = f"""
👤 Profile

Name : {user.first_name}

Username : @{user.username or "None"}

User ID :
`{user.id}`
"""

        return await callback.message.edit_text(
            text,
            reply_markup=back_button("user_dashboard")
        )

    # ===============================
    # ABOUT
    # ===============================

    if data == "about":

        return await callback.message.edit_text(
            """
🤖 AutoJoinBot

Version : 1.0

Features

• Auto Join Approve

• Unlimited Channels

• Unlimited Owners

• MongoDB

• Render Ready

• GitHub Ready
""",
            reply_markup=back_button("user_dashboard")
        )

    # ===============================
    # SUPPORT
    # ===============================

    if data == "support":

        return await callback.answer(
            "Support Coming Soon.",
            show_alert=True
        )

    # ===============================
    # OWNER PANEL
    # ===============================

    if data == "owner_panel":

        if not await is_owner(user.id):

            return await callback.answer(
                "Access Denied",
                show_alert=True
            )

        return await callback.message.edit_text(
            "👑 Owner Dashboard",
            reply_markup=owner_dashboard()
        )

    # ===============================
    # STATISTICS
    # ===============================

    if data == "stats":

        if not await is_owner(user.id):
            return

        total_users = await users.count_documents({})
        total_channels = await channels.count_documents({})
        total_requests = await join_requests.count_documents({})
        total_owners = await owners.count_documents({})

        text = f"""
📊 Bot Statistics

👥 Users :
{total_users}

👑 Owners :
{total_owners}

📢 Channels :
{total_channels}

📥 Join Requests :
{total_requests}
"""

        return await callback.message.edit_text(
            text,
            reply_markup=back_button("owner_panel")
        )

    # ===============================
    # OWNERS
    # ===============================

    if data == "owners":

        if not await is_owner(user.id):
            return

        text = "👑 Owners\n\n"

        async for owner in owners.find():

            text += f"• `{owner['user_id']}`\n"

        return await callback.message.edit_text(
            text,
            reply_markup=back_button("owner_panel")
        )

    # ===============================
    # CHANNELS
    # ===============================

    if data == "channels":

        if not await is_owner(user.id):
            return

        text = "📢 Connected Channels\n\n"

        count = 0

        async for channel in channels.find():

            count += 1

            text += (
                f"• {channel.get('title','Unknown')}\n"
                f"`{channel['chat_id']}`\n\n"
            )

        if count == 0:
            text += "No channels connected."

        return await callback.message.edit_text(
            text,
            reply_markup=channel_panel()
        )

    # ===============================
    # ADD CHANNEL
    # ===============================

    if data == "add_channel":

        text = """
📢 How To Add Channel

1️⃣ Add the bot as Admin.

2️⃣ Give permission:

✅ Manage Join Requests

3️⃣ Send one Join Request.

Done.

The bot registers the channel automatically.
"""

        return await callback.message.edit_text(
            text,
            reply_markup=back_button("channels")
        )

    # ===============================
    # BOT INFO
    # ===============================

    if data == "bot_info":

        text = """
🤖 AutoJoinBot

Version : 1.0

Python

Pyrogram

MongoDB

Render

GitHub

Made with ❤️
"""

        return await callback.message.edit_text(
            text,
            reply_markup=back_button("owner_panel")
        )

    # ===============================
    # UNKNOWN
    # ===============================

    return await callback.answer("Unknown Button")
