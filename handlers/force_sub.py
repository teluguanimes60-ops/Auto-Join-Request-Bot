from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database.models import (
    get_force_channels,
)


# ==========================================================
# Check Force Subscribe
# ==========================================================

async def check_force_sub(
    client: Client,
    user_id: int,
    channel_id: int,
):

    force_channels = await get_force_channels(channel_id)

    if not force_channels:
        return True

    for ch in force_channels:

        try:
            member = await client.get_chat_member(
                ch,
                user_id
            )

            if member.status.name in (
                "LEFT",
                "BANNED",
            ):
                return False

        except Exception:
            return False

    return True


# ==========================================================
# Send Force Subscribe Message
# ==========================================================

async def send_force_sub(
    message,
    channel_id,
):

    force_channels = await get_force_channels(channel_id)

    buttons = []

    for ch in force_channels:

        username = str(ch).replace("@", "")

        buttons.append(
            [
                InlineKeyboardButton(
                    f"📢 {username}",
                    url=f"https://t.me/{username}",
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                "✅ I've Joined",
                callback_data=f"check_sub:{channel_id}",
            )
        ]
    )

    await message.reply_text(
        "🚫 You must join all required channels before using this bot.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


# ==========================================================
# Verify Subscription
# ==========================================================

@Client.on_callback_query()
async def force_sub_callback(
    client: Client,
    query: CallbackQuery,
):

    if not query.data.startswith("check_sub:"):
        return

    channel_id = int(
        query.data.split(":")[1]
    )

    ok = await check_force_sub(
        client,
        query.from_user.id,
        channel_id,
    )

    if ok:

        return await query.answer(
            "✅ Subscription Verified!",
            show_alert=True,
        )

    await query.answer(
        "❌ Join all required channels first.",
        show_alert=True,
    )
