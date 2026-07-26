from pyrogram import Client
from pyrogram.types import CallbackQuery

from database import users, owners, channels, join_requests
from utils.permissions import is_owner
from utils.keyboards import owner_dashboard, user_dashboard


@Client.on_callback_query()
async def callback_handler(client: Client, callback: CallbackQuery):

    data = callback.data
    user = callback.from_user

    # ==========================
    # CLOSE
    # ==========================
    if data == "close":
        return await callback.message.delete()

    # ==========================
    # USER HOME
    # ==========================
    elif data == "user_dashboard":

        return await callback.message.edit_text(
            f"👋 Welcome **{user.first_name}**",
            reply_markup=user_dashboard()
        )

    # ==========================
    # OWNER HOME
    # ==========================
    elif data == "owner_panel":

        if not await is_owner(user.id):
            return await callback.answer(
                "Access Denied",
                show_alert=True
            )

        return await callback.message.edit_text(
            "👑 **Owner Dashboard**",
            reply_markup=owner_dashboard()
        )

    # ==========================
    # STATISTICS
    # ==========================
    elif data == "stats":

        if not await is_owner(user.id):
            return

        total_users = await users.count_documents({})
        total_channels = await channels.count_documents({})
        total_requests = await join_requests.count_documents({})
        total_owners = await owners.count_documents({})

        text = f"""
📊 **Statistics**

👥 Users : `{total_users}`
👑 Owners : `{total_owners}`
📢 Channels : `{total_channels}`
📥 Requests : `{total_requests}`
"""

        return await callback.message.edit_text(
            text,
            reply_markup=owner_dashboard()
        )

    # ==========================
    # OWNERS
    # ==========================
    elif data == "owners":

        if not await is_owner(user.id):
            return

        owner_text = ""

        async for owner in owners.find():
            owner_text += f"• `{owner['user_id']}`\n"

        if not owner_text:
            owner_text = "No Owners."

        return await callback.message.edit_text(
            f"👑 **Owners**\n\n{owner_text}",
            reply_markup=owner_dashboard()
        )

    # ==========================
    # CHANNELS
    # ==========================
    elif data == "channels":

        if not await is_owner(user.id):
            return

        total = await channels.count_documents({})

        return await callback.message.edit_text(
            f"📢 Connected Channels\n\nTotal : `{total}`",
            reply_markup=owner_dashboard()
        )

    # ==========================
    # BROADCAST
    # ==========================
    elif data == "broadcast":

        return await callback.answer(
            "Coming Soon",
            show_alert=True
        )

    # ==========================
    # SETTINGS
    # ==========================
    elif data == "settings":

        return await callback.answer(
            "Coming Soon",
            show_alert=True
        )

    # ==========================
    # BACKUP
    # ==========================
    elif data == "backup":

        return await callback.answer(
            "Coming Soon",
            show_alert=True
        )

    # ==========================
    # LOGS
    # ==========================
    elif data == "logs":

        return await callback.answer(
            "Coming Soon",
            show_alert=True
        )

    # ==========================
    # BOT INFO
    # ==========================
    elif data == "bot_info":

        text = """
🤖 **AutoJoinBot**

Version : 1.0

Hosted on Render

Database : MongoDB Atlas

Framework : Pyrogram
"""

        return await callback.message.edit_text(
            text,
            reply_markup=owner_dashboard()
        )

    # ==========================
    # UNKNOWN
    # ==========================
    else:
        return await callback.answer("Unknown Button")
