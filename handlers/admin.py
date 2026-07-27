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
    is_admin,
    ban_user,
    unban_user,
    get_stats,
)

from database.mongo import (
    users,
    admins,
)


# ==========================================
# Add Admin (Owner Only)
# ==========================================

@Client.on_message(filters.command("addadmin") & filters.private)
async def add_admin_cmd(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/addadmin USER_ID"
        )

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("Invalid User ID.")

    await add_admin(user_id)

    await message.reply_text(
        f"✅ {user_id} is now an admin."
    )


# ==========================================
# Remove Admin
# ==========================================

@Client.on_message(filters.command("removeadmin") & filters.private)
async def remove_admin_cmd(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    if len(message.command) != 2:
        return

    user_id = int(message.command[1])

    await remove_admin(user_id)

    await message.reply_text(
        "✅ Admin removed."
    )


# ==========================================
# List Admins
# ==========================================

@Client.on_message(filters.command("admins") & filters.private)
async def admins_list(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    text = "🛡 Admin List\n\n"

    async for admin in admins.find({}):

        text += f"• `{admin['user_id']}`\n"

    await message.reply_text(text)


# ==========================================
# Ban User
# ==========================================

@Client.on_message(filters.command("ban") & filters.private)
async def ban_user_cmd(client: Client, message: Message):

    if not (
        message.from_user.id == OWNER_ID
        or await is_admin(message.from_user.id)
    ):
        return

    if len(message.command) != 2:
        return

    user_id = int(message.command[1])

    await ban_user(user_id)

    await message.reply_text(
        "✅ User banned."
    )


# ==========================================
# Unban User
# ==========================================

@Client.on_message(filters.command("unban") & filters.private)
async def unban_user_cmd(client: Client, message: Message):

    if not (
        message.from_user.id == OWNER_ID
        or await is_admin(message.from_user.id)
    ):
        return

    if len(message.command) != 2:
        return

    user_id = int(message.command[1])

    await unban_user(user_id)

    await message.reply_text(
        "✅ User unbanned."
    )


# ==========================================
# Statistics
# ==========================================

@Client.on_message(filters.command("stats") & filters.private)
async def stats(client: Client, message: Message):

    if not (
        message.from_user.id == OWNER_ID
        or await is_admin(message.from_user.id)
    ):
        return

    stats = await get_stats()

    text = f"""
📊 Bot Statistics

👥 Users : {stats['users']}

🛡 Admins : {stats['admins']}

📢 Channels : {stats['channels']}

✅ Accepted Joins : {stats['joins']}
"""

    await message.reply_text(text)


# ==========================================
# Users List
# ==========================================

@Client.on_message(filters.command("users") & filters.private)
async def users_list(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    text = "👥 Registered Users\n\n"

    count = 0

    async for user in users.find({}):

        count += 1

        text += (
            f"{count}. "
            f"`{user['user_id']}`\n"
        )

        if count == 50:
            break

    text += "\nShowing first 50 users."

    await message.reply_text(text)


# ==========================================
# Broadcast
# ==========================================

@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast(client: Client, message: Message):

    if message.from_user.id != OWNER_ID:
        return

    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message with /broadcast"
        )

    sent = 0
    failed = 0

    async for user in users.find({}):

        try:

            await message.reply_to_message.copy(
                user["user_id"]
            )

            sent += 1

        except Exception:

            failed += 1

    await message.reply_text(
        f"""
📢 Broadcast Finished

✅ Sent : {sent}

❌ Failed : {failed}
"""
    )


# ==========================================
# Admin Panel Command
# ==========================================

@Client.on_message(filters.command("panel") & filters.private)
async def panel(client: Client, message: Message):

    if not (
        message.from_user.id == OWNER_ID
        or await is_admin(message.from_user.id)
    ):
        return

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📊 Statistics",
                    callback_data="stats",
                )
            ],
            [
                InlineKeyboardButton(
                    "📂 Channels",
                    callback_data="my_channels",
                )
            ],
            [
                InlineKeyboardButton(
                    "⚙ Settings",
                    callback_data="settings",
                )
            ],
        ]
    )

    await message.reply_text(
        "🛡 Admin Panel",
        reply_markup=keyboard,
    )
