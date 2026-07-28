from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from config import MONGO_URI

client = None
db = None

users = None
admins = None
channels = None
settings = None
joins = None
banned_users = None
broadcast_logs = None


async def connect_db():
    global client
    global db
    global users
    global admins
    global channels
    global settings
    global joins
    global banned_users
    global broadcast_logs

    try:
        client = AsyncIOMotorClient(MONGO_URI)

        await client.admin.command("ping")

        db = client["AutoJoinBot"]

        users = db["users"]
        admins = db["admins"]
        channels = db["channels"]
        settings = db["settings"]
        joins = db["join_logs"]
        banned_users = db["banned_users"]
        broadcast_logs = db["broadcast_logs"]

        await users.create_index("user_id", unique=True)
        await admins.create_index("user_id", unique=True)
        await channels.create_index("channel_id", unique=True)

        print("✅ MongoDB Connected Successfully")

    except ConnectionFailure as e:
        print("❌ MongoDB Connection Failed")
        print(e)
        raise

    except Exception as e:
        print("❌ Database Error")
        print(e)
        raise


def get_db():
    return db
