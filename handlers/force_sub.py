from pyrogram import Client
from pyrogram.types import CallbackQuery

from config import FORCE_SUB_CHANNEL


# ==========================================================
# Force Subscribe
# ==========================================================

async def check_force_sub(client, user_id):

    if not FORCE_SUB_CHANNEL:
        return True

    try:

        member = await client.get_chat_member(
            FORCE_SUB_CHANNEL,
            user_id
        )

        if member:
            return True

    except Exception:
        return False

    return False


# ==========================================================
# Subscribe Button
# ==========================================================

@Client.on_callback_query()
async def force_sub_callback(client: Client, query: CallbackQuery):

    if query.data != "check_sub":
        return

    ok = await check_force_sub(
        client,
        query.from_user.id
    )

    if ok:

        await query.answer(
            "✅ Subscription Verified!",
            show_alert=True
        )

        return

    await query.answer(
        "❌ Please join the required channel first.",
        show_alert=True
    )
