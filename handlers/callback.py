from pyrogram import Client
from pyrogram.types import CallbackQuery

from utils.keyboards import (
    owner_dashboard,
    user_dashboard
)


@Client.on_callback_query()
async def callback_handler(client: Client, callback: CallbackQuery):
    data = callback.data
    user = callback.from_user

    # =========================
    # Close Message
    # =========================
    if data == "close":
        await callback.message.delete()
        return

    # =========================
    # Back to Home
    # =========================
    if data == "home":
        await callback.message.edit_text(
            f"👋 Welcome back, **{user.first_name}**!",
            reply_markup=user_dashboard()
        )
        return

    # =========================
    # Owner Dashboard
    # =========================
    if data == "owner_panel":
        await callback.message.edit_text(
            "👑 **Owner Dashboard**\n\n"
            "Choose an option below.",
            reply_markup=owner_dashboard()
        )
        return

    # =========================
    # User Dashboard
    # =========================
    if data == "user_dashboard":
        await callback.message.edit_text(
            "👤 **User Dashboard**\n\n"
            "Choose an option below.",
            reply_markup=user_dashboard()
        )
        return

    # =========================
    # Profile
    # =========================
    if data == "profile":
        text = (
            f"👤 **Your Profile**\n\n"
            f"🆔 ID: `{user.id}`\n"
            f"👤 Name: {user.first_name}\n"
            f"📛 Username: @{user.username if user.username else 'None'}"
        )

        await callback.message.edit_text(
            text,
            reply_markup=user_dashboard()
        )
        return

    # =========================
    # About
    # =========================
    if data == "about":
        await callback.answer(
            "AutoJoinBot v1.0",
            show_alert=True
        )
        return

    # =========================
    # Support
    # =========================
    if data == "support":
        await callback.answer(
            "Support system coming soon.",
            show_alert=True
        )
        return

    # =========================
    # Statistics
    # =========================
    if data == "stats":
        await callback.answer(
            "Statistics panel coming soon.",
            show_alert=True
        )
        return

    # =========================
    # Settings
    # =========================
    if data == "settings":
        await callback.answer(
            "Settings panel coming soon.",
            show_alert=True
        )
        return

    # =========================
    # Channels
    # =========================
    if data == "channels":
        await callback.answer(
            "Channel manager coming soon.",
            show_alert=True
        )
        return

    # =========================
    # Owners
    # =========================
    if data == "owners":
        await callback.answer(
            "Owner manager coming soon.",
            show_alert=True
        )
        return

    # =========================
    # Broadcast
    # =========================
    if data == "broadcast":
        await callback.answer(
            "Broadcast system coming soon.",
            show_alert=True
        )
        return

    # =========================
    # Backup
    # =========================
    if data == "backup":
        await callback.answer(
            "Backup system coming soon.",
            show_alert=True
        )
        return

    # =========================
    # Unknown Callback
    # =========================
    await callback.answer(
        "Unknown action.",
        show_alert=True
    )
