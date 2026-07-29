from datetime import datetime

from database.mongo import (
    users,
    admins,
    channels,
    join_logs,
    banned_users,
)

# ==========================================================
# USERS
# ==========================================================

async def add_user(user):
    await users.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "user_id": user.id,
                "name": user.first_name,
                "username": user.username,
                "joined": datetime.utcnow(),
            }
        },
        upsert=True,
    )


# ==========================================================
# CHANNELS
# ==========================================================

async def add_channel(chat, owner_id=None):
    """
    Register a channel.

    owner_id = Telegram user who added the channel.
    """

    await channels.update_one(
        {"channel_id": chat.id},
        {
            "$set": {
                "channel_id": chat.id,
                "owner_id": owner_id,
                "title": chat.title,
                "username": chat.username,

                # Main Features
                "auto_accept": True,
                "welcome": True,

                "welcome_text":
                "👋 Welcome {mention} to {channel}!",

                "auto_delete": False,
                "delete_time": 30,

                # Public Bot Features
                "force_sub": False,

                # Every owner can configure
                # their own required channels.
                "force_channels": [],

                "created_at": datetime.utcnow(),
            }
        },
        upsert=True,
    )


async def get_channel(channel_id):
    return await channels.find_one(
        {"channel_id": channel_id}
    )


async def all_channels():
    return await channels.find().to_list(length=None)


async def remove_channel(channel_id):
    await channels.delete_one(
        {"channel_id": channel_id}
    )


async def update_channel_setting(
    channel_id,
    key,
    value,
):
    await channels.update_one(
        {"channel_id": channel_id},
        {
            "$set": {
                key: value
            }
        }
    )


# ==========================================================
# FORCE SUB CHANNELS
# ==========================================================

async def set_force_channels(
    channel_id,
    force_channels: list,
):
    """
    Save owner's Force Subscribe channels.

    Example:
    [
        "@channel1",
        "@channel2",
        "@channel3",
        "@channel4"
    ]
    """

    await channels.update_one(
        {"channel_id": channel_id},
        {
            "$set": {
                "force_channels": force_channels
            }
        }
    )


async def get_force_channels(channel_id):

    data = await channels.find_one(
        {"channel_id": channel_id}
    )

    if not data:
        return []

    return data.get(
        "force_channels",
        [],
    )


# ==========================================================
# ADMINS
# ==========================================================

async def add_admin(user_id):
    await admins.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id
            }
        },
        upsert=True,
    )


async def remove_admin(user_id):
    await admins.delete_one(
        {"user_id": user_id}
    )


async def is_admin(user_id):
    return await admins.find_one(
        {"user_id": user_id}
    )


# ==========================================================
# BANNED USERS
# ==========================================================

async def ban_user(user_id):
    await banned_users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id
            }
        },
        upsert=True,
    )


async def unban_user(user_id):
    await banned_users.delete_one(
        {"user_id": user_id}
    )


async def is_banned(user_id):
    return await banned_users.find_one(
        {"user_id": user_id}
    )


# ==========================================================
# JOIN LOGS
# ==========================================================

async def log_join(channel_id, user_id):
    await join_logs.insert_one(
        {
            "channel_id": channel_id,
            "user_id": user_id,
            "time": datetime.utcnow(),
        }
    )


# ==========================================================
# STATISTICS
# ==========================================================

async def get_stats():
    return {
        "users": await users.count_documents({}),
        "admins": await admins.count_documents({}),
        "channels": await channels.count_documents({}),
        "joins": await join_logs.count_documents({}),
    }
