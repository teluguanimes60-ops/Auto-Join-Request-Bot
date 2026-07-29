import os

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import OWNER_ID

from database.models import (
    add_admin,
    remove_admin,
    get_stats,
)

from database.mongo import (
    users,
    admins,
    channels,
    banned_users,
)


# ==========================================================
# Owner Filter
# ==========================================================

def owner_only(func):
    async def wrapper(client, message):
        if message.from_user.id != OWNER_ID:
            return

        return await func(client, message)

    return wrapper


# ==========================================================
# Owner Panel
# ==========================================================

@Client.on_message(filters.private & filters.command("owner"))
@owner_only
async def owner_panel(client: Client, message: Message):

    stats = await get_stats()

    text = f"""
👑 Owner Control Panel

━━━━━━━━━━━━━━━━━━

👥 Users      : {stats['users']}
🛡 Admins     : {stats['admins']}
📢 Channels   : {stats['channels']}
✅ Join Logs  : {stats['joins']}

━━━━━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👥 Users",
                    callback_data="owner_users",
                ),
                InlineKeyboardButton(
                    "🛡 Admins",
                    callback_data="owner_admins",
                ),
            ],
            [
                InlineKeyboardButton(
                    "📊 Statistics",
                    callback_data="stats",
                ),
                InlineKeyboardButton(
                    "📢 Broadcast",
                    callback_data="broadcast",
                ),
            ],
            [
                InlineKeyboardButton(
                    "🚫 Banned Users",
                    callback_data="banned_users",
                )
            ],
        ]
    )

    await message.reply_text(
        text,
        reply_markup=keyboard,
    )


# ==========================================================
# Promote Admin
# ==========================================================

@Client.on_message(filters.private & filters.command("promote"))
@owner_only
async def promote_admin(client, message):

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/promote USER_ID"
        )

    try:
        user_id = int(message.command[1])

    except ValueError:

        return await message.reply_text(
            "Invalid User ID."
        )

    await add_admin(user_id)

    await message.reply_text(
        f"✅ {user_id} promoted successfully."
    )


# ==========================================================
# Demote Admin
# ==========================================================

@Client.on_message(filters.private & filters.command("demote"))
@owner_only
async def demote_admin(client, message):

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/demote USER_ID"
        )

    try:
        user_id = int(message.command[1])

    except ValueError:

        return await message.reply_text(
            "Invalid User ID."
        )

    if user_id == OWNER_ID:

        return await message.reply_text(
            "❌ Owner cannot be removed."
        )

    await remove_admin(user_id)

    await message.reply_text(
        "✅ Admin removed."
    )


# ==========================================================
# Database Statistics
# ==========================================================

@Client.on_message(filters.private & filters.command("dbstats"))
@owner_only
async def db_stats(client, message):

    stats = await get_stats()

    banned = await banned_users.count_documents({})

    text = f"""
📊 Database Statistics

👥 Users      : {stats['users']}
🛡 Admins     : {stats['admins']}
📢 Channels   : {stats['channels']}
✅ Join Logs  : {stats['joins']}
🚫 Banned     : {banned}
"""

    await message.reply_text(text)


# ==========================================================
# Export Users
# ==========================================================

@Client.on_message(filters.private & filters.command("export_users"))
@owner_only
async def export_users(client, message):

    filename = "users.txt"

    with open(filename, "w", encoding="utf-8") as f:

        async for user in users.find():

            f.write(f"{user.get('user_id')}\n")

    await message.reply_document(
        filename,
        caption="👥 User Database",
    )

    os.remove(filename)


# ==========================================================
# Export Channels
# ==========================================================

@Client.on_message(filters.private & filters.command("export_channels"))
@owner_only
async def export_channels(client, message):

    filename = "channels.txt"

    with open(filename, "w", encoding="utf-8") as f:

        async for ch in channels.find():

            f.write(
                f"{ch.get('title','Unknown')} | "
                f"{ch.get('channel_id')}\n"
            )

    await message.reply_document(
        filename,
        caption="📢 Channels",
    )

    os.remove(filename)


# ==========================================================
# Export Admins
# ==========================================================

@Client.on_message(filters.private & filters.command("export_admins"))
@owner_only
async def export_admins(client, message):

    filename = "admins.txt"

    with open(filename, "w", encoding="utf-8") as f:

        async for admin in admins.find():

            f.write(
                f"{admin.get('user_id')}\n"
            )

    await message.reply_document(
        filename,
        caption="🛡 Admin List",
    )

    os.remove(filename)
