from config import OWNER_ID
from database.models import is_admin


# ==========================================================
# Owner
# ==========================================================

def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


# ==========================================================
# Admin
# ==========================================================

async def has_admin_access(user_id: int) -> bool:

    if user_id == OWNER_ID:
        return True

    return bool(await is_admin(user_id))


# ==========================================================
# Owner Only
# ==========================================================

async def owner_only(message):

    if message.from_user.id != OWNER_ID:
        await message.reply_text(
            "❌ Only the bot owner can use this."
        )
        return False

    return True


# ==========================================================
# Admin Only
# ==========================================================

async def admin_only(message):

    if message.from_user.id == OWNER_ID:
        return True

    if await is_admin(message.from_user.id):
        return True

    await message.reply_text(
        "❌ Only admins can use this."
    )

    return False
