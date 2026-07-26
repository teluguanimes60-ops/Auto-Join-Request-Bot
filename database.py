from motor.motor_asyncio import AsyncIOMotorClient
from config import config


# MongoDB Client
client = AsyncIOMotorClient(config.MONGO_URI)

# Database
db = client[config.DATABASE_NAME]

# Collections
owners = db["owners"]
users = db["users"]
channels = db["channels"]
settings = db["settings"]
join_requests = db["join_requests"]
logs = db["logs"]
broadcasts = db["broadcasts"]
stats = db["stats"]


async def setup_database():
    """
    Create indexes and ensure the first owner exists.
    """

    # Users
    await users.create_index("user_id", unique=True)

    # Owners
    await owners.create_index("user_id", unique=True)

    # Channels
    await channels.create_index("chat_id", unique=True)

    # Join Requests
    await join_requests.create_index("request_id", unique=True)

    # Logs
    await logs.create_index("time")

    # Statistics
    await stats.create_index("date")

    # Add the permanent owner if not already present
    owner = await owners.find_one({"user_id": config.OWNER_ID})

    if not owner:
        await owners.insert_one({
            "user_id": config.OWNER_ID,
            "role": "owner",
            "added_by": "system"
        })

    print("✅ Database connected successfully.")
