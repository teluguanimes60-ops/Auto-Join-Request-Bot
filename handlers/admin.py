from pyrogram import Client, filters
from pyrogram.types import Message

from database import owners
from utils.permissions import is_owner


@Client.on_message(filters.private & filters.command("addowner"))
async def add_owner(client: Client, message: Message):

    if not await is_owner(message.from_user.id):
        return await message.reply_text("❌ Access Denied.")

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/addowner USER_ID"
        )

    try:
        user_id = int(message.command[1])
    except:
        return await message.reply_text("Invalid User ID.")

    already = await owners.find_one({"user_id": user_id})

    if already:
        return await message.reply_text("Already an owner.")

    await owners.insert_one(
        {
            "user_id": user_id
        }
    )

    await message.reply_text(
        f"✅ {user_id} is now an Owner."
    )


@Client.on_message(filters.private & filters.command("removeowner"))
async def remove_owner(client: Client, message: Message):

    if not await is_owner(message.from_user.id):
        return await message.reply_text("❌ Access Denied.")

    if len(message.command) != 2:
        return await message.reply_text(
            "Usage:\n/removeowner USER_ID"
        )

    try:
        user_id = int(message.command[1])
    except:
        return await message.reply_text("Invalid User ID.")

    await owners.delete_one(
        {
            "user_id": user_id
        }
    )

    await message.reply_text(
        f"✅ Removed Owner {user_id}"
    )


@Client.on_message(filters.private & filters.command("owners"))
async def owner_list(client: Client, message: Message):

    if not await is_owner(message.from_user.id):
        return

    text = "👑 Owners\n\n"

    async for owner in owners.find():
        text += f"• `{owner['user_id']}`\n"

    await message.reply_text(text)
