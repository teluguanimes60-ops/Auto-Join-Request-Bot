from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

from config import MONGO_URI

# ==========================
# MongoDB Connection
# ==========================

client = AsyncIOMotorClient(MONGO_URI)

db = client["AutoJoinBot"]

users_col = db["users"]
channels_col = db["channels"]
settings_col = db["settings"]
logs_col = db["logs"]

# ==========================================================
# USERS
# ==========================================================

async def add_user(user):
    await users_col.update_one(
        {"user_id": user.id},
        {
            "$set": {
                "user_id": user.id,
                "first_name": user.first_name,
                "username": user.username,
                "date": datetime.utcnow()
            }
        },
        upsert=True
    )


async def get_user(user_id):
    return await users_col.find_one({"user_id": user_id})


async def total_users():
    return await users_col.count_documents({})


async def all_users():
    return users_col.find({})


# ==========================================================
# CHANNELS
# ==========================================================

async def add_channel(owner_id, chat):

    data = {
        "channel_id": chat.id,
        "title": chat.title,
        "username": chat.username,
        "owner": owner_id,
        "delay": 60,
        "welcome": "",
        "status": True,
        "date": datetime.utcnow()
    }

    await channels_col.update_one(
        {"channel_id": chat.id},
        {"$set": data},
        upsert=True
    )


async def get_channel(channel_id):
    return await channels_col.find_one(
        {"channel_id": channel_id}
    )


async def get_owner_channels(owner_id):

    cursor = channels_col.find(
        {"owner": owner_id}
    )

    return await cursor.to_list(length=100)


async def remove_channel(channel_id):

    await channels_col.delete_one(
        {"channel_id": channel_id}
    )


async def total_channels():
    return await channels_col.count_documents({})


async def all_channels():
    return channels_col.find({})


# ==========================================================
# DELAY
# ==========================================================

async def set_delay(channel_id, seconds):

    await channels_col.update_one(
        {"channel_id": channel_id},
        {
            "$set": {
                "delay": seconds
            }
        }
    )


async def get_delay(channel_id):

    channel = await get_channel(channel_id)

    if not channel:
        return 60

    return channel.get("delay", 60)


# ==========================================================
# WELCOME MESSAGE
# ==========================================================

async def set_welcome(channel_id, text):

    await channels_col.update_one(
        {"channel_id": channel_id},
        {
            "$set": {
                "welcome": text
            }
        }
    )


async def get_welcome(channel_id):

    channel = await get_channel(channel_id)

    if not channel:
        return ""

    return channel.get("welcome", "")


# ==========================================================
# ENABLE / DISABLE
# ==========================================================

async def set_status(channel_id, value):

    await channels_col.update_one(
        {"channel_id": channel_id},
        {
            "$set": {
                "status": value
            }
        }
    )


async def get_status(channel_id):

    channel = await get_channel(channel_id)

    if not channel:
        return False

    return channel.get("status", False)


# ==========================================================
# LOGS
# ==========================================================

async def add_log(text):

    await logs_col.insert_one(
        {
            "text": text,
            "date": datetime.utcnow()
        }
    )


async def latest_logs(limit=50):

    cursor = logs_col.find().sort(
        "_id",
        -1
    ).limit(limit)

    return await cursor.to_list(length=limit)


# ==========================================================
# SETTINGS
# ==========================================================

async def save_setting(key, value):

    await settings_col.update_one(
        {"key": key},
        {
            "$set": {
                "value": value
            }
        },
        upsert=True
    )


async def get_setting(key, default=None):

    data = await settings_col.find_one(
        {"key": key}
    )

    if not data:
        return default

    return data["value"]


# ==========================================================
# STATISTICS
# ==========================================================

async def get_stats():

    return {
        "users": await total_users(),
        "channels": await total_channels(),
        "logs": await logs_col.count_documents({})
    }

# ==========================================================
# CHANNEL EXISTS
# ==========================================================

async def channel_exists(channel_id):

    return await channels_col.find_one(
        {
            "channel_id": channel_id
        }
    )


# ==========================================================
# UPDATE CHANNEL
# ==========================================================

async def update_channel(channel_id, data):

    await channels_col.update_one(
        {
            "channel_id": channel_id
        },
        {
            "$set": data
        }
    )


# ==========================================================
# DELETE ALL LOGS
# ==========================================================

async def clear_logs():

    await logs_col.delete_many({})


# ==========================================================
# TOTAL LOGS
# ==========================================================

async def total_logs():

    return await logs_col.count_documents({})
