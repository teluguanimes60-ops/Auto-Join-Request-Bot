from datetime import datetime

from .mongo import (
    users,
    admins,
    channels,
    settings,
    join_logs,
    banned_users,
    broadcast_logs,
)

# ==========================================
# Users
# ==========================================

async def add_user(user):
    await users.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "user_id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "is_bot": user.is_bot,
                "joined_on": datetime.utcnow(),
            }
        },
        upsert=True,
    )


async def get_user(user_id):
    return await users.find_one({"user_id": user_id})


async def total_users():
    return await users.count_documents({})


# ==========================================
# Ban Users
# ==========================================

async def ban_user(user_id):
    await banned_users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "banned_on": datetime.utcnow(),
            }
        },
        upsert=True,
    )


async def unban_user(user_id):
    await banned_users.delete_one({"user_id": user_id})


async def is_banned(user_id):
    return await banned_users.find_one({"user_id": user_id}) is not None


# ==========================================
# Admins
# ==========================================

async def add_admin(user_id):
    await admins.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "added_on": datetime.utcnow(),
            }
        },
        upsert=True,
    )


async def remove_admin(user_id):
    await admins.delete_one({"user_id": user_id})


async def is_admin(user_id):
    return await admins.find_one({"user_id": user_id}) is not None


async def total_admins():
    return await admins.count_documents({})


# ==========================================
# Channels
# ==========================================

async def add_channel(channel):
    await channels.update_one(
        {"channel_id": channel.id},
        {
            "$set": {
                "channel_id": channel.id,
                "title": channel.title,
                "username": channel.username,
                "added_on": datetime.utcnow(),
                "auto_accept": True,
                "welcome": True,
                "auto_delete": False,
            }
        },
        upsert=True,
    )


async def remove_channel(channel_id):
    await channels.delete_one({"channel_id": channel_id})


async def get_channel(channel_id):
    return await channels.find_one({"channel_id": channel_id})


async def total_channels():
    return await channels.count_documents({})


async def all_channels():
    cursor = channels.find({})
    return await cursor.to_list(length=None)


# ==========================================
# Channel Settings
# ==========================================

async def update_channel_setting(channel_id, key, value):
    await channels.update_one(
        {"channel_id": channel_id},
        {"$set": {key: value}},
    )


# ==========================================
# Join Logs
# ==========================================

async def log_join(channel_id, user_id):
    await join_logs.insert_one(
        {
            "channel_id": channel_id,
            "user_id": user_id,
            "accepted_at": datetime.utcnow(),
        }
    )


async def total_joins():
    return await join_logs.count_documents({})


# ==========================================
# Global Settings
# ==========================================

async def get_setting(key):
    data = await settings.find_one({"key": key})
    if data:
        return data["value"]
    return None


async def set_setting(key, value):
    await settings.update_one(
        {"key": key},
        {
            "$set": {
                "key": key,
                "value": value,
            }
        },
        upsert=True,
    )


# ==========================================
# Broadcast Logs
# ==========================================

async def save_broadcast(message_id, total):
    await broadcast_logs.insert_one(
        {
            "message_id": message_id,
            "total_users": total,
            "sent_at": datetime.utcnow(),
        }
    )


# ==========================================
# Statistics
# ==========================================

async def get_stats():
    return {
        "users": await total_users(),
        "admins": await total_admins(),
        "channels": await total_channels(),
        "joins": await total_joins(),
    }
