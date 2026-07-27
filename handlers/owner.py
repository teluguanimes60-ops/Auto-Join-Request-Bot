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


# ==========================================
# Owner Filter
# ==========================================

def owner_only(func):
    async def wrapper(client, message):
        if message.from_user.id != OWNER_ID:
            return
        return await func(client, message)
    return wrapper


# ==========================================
# Owner Panel
# ==========================================

@Client.on_message(filters.private & filters.command("owner"))
@owner_only
async def owner_panel(client: Client, message: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👥 Users",
                    callback_data="owner_users"
                ),
                InlineKeyboardButton(
                    "🛡 Admins",
                    callback_data="owner_admins"
                )
            ],
            [
                InlineKeyboardButton(
                    "📢 Broadcast",
                    callback_data="broadcast"
                ),
                InlineKeyboardButton(
                    "📊 Statistics",
                    callback_data="stats"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚫 Banned Users",
                    callback_data="banned_users"
                )
            ],
            [
                InlineKeyboardButton(
                    "⚙ Settings",
                    callback_data="owner_settings"
                )
            ]
        ]
    )

    await message.reply_text(
        "👑 **Owner Control Panel**",
        reply_markup=keyboard
    )


# ==========================================
# Add Admin
# ==========================================

@Client.on_message(filters.private & filters.command("promote"))
@owner_only
async def promote_admin(client, message):

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/promote USER_ID"
        )

    user_id = int(message.command[1])

    await add_admin(user_id)

    await message.reply_text(
        "✅ Admin added successfully."
    )


# ==========================================
# Remove Admin
# ==========================================

@Client.on_message(filters.private & filters.command("demote"))
@owner_only
async def demote_admin(client, message):

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/demote USER_ID"
        )

    user_id = int(message.command[1])

    await remove_admin(user_id)

    await message.reply_text(
        "✅ Admin removed."
    )


# ==========================================
# Database Statistics
# ==========================================

@Client.on_message(filters.private & filters.command("dbstats"))
@owner_only
async def db_stats(client, message):

    stats = await get_stats()

    banned = await banned_users.count_documents({})

    text = f"""
📊 Database Statistics

👥 Users : {stats['users']}

🛡 Admins : {stats['admins']}

📢 Channels : {stats['channels']}

✅ Accepted : {stats['joins']}

🚫 Banned : {banned}
"""

    await message.reply_text(text)


# ==========================================
# Export Users
# ==========================================

@Client.on_message(filters.private & filters.command("export_users"))
@owner_only
async def export_users(client, message):

    text = ""

    async for user in users.find():

        text += f"{user['user_id']}\n"

    if not text:
        text = "No users found."

    with open("users.txt", "w") as f:
        f.write(text)

    await message.reply_document(
        "users.txt",
        caption="👥 User Database"
    )


# ==========================================
# Export Channels
# ==========================================

@Client.on_message(filters.private & filters.command("export_channels"))
@owner_only
async def export_channels(client, message):

    text = ""

    async for ch in channels.find():

        text += (
            f"{ch['title']} | "
            f"{ch['channel_id']}\n"
        )

    if not text:
        text = "No channels."

    with open("channels.txt", "w") as f:
        f.write(text)

    await message.reply_document(
        "channels.txt",
        caption="📢 Channels"
    )


# ==========================================
# Export Admins
# ==========================================

@Client.on_message(filters.private & filters.command("export_admins"))
@owner_only
async def export_admins(client, message):

    text = ""

    async for admin in admins.find():

        text += f"{admin['user_id']}\n"

    if not text:
        text = "No admins."

    with open("admins.txt", "w") as f:
        f.write(text)

    await message.reply_document(
        "admins.txt",
        caption="🛡 Admin List"
    )
