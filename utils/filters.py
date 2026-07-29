from pyrogram import filters

from config import OWNER_ID
from database.models import is_admin, is_banned


# ==========================================================
# Owner Filter
# ==========================================================

async def owner_filter(_, __, message):

    return (
        message.from_user
        and message.from_user.id == OWNER_ID
    )


owner = filters.create(owner_filter)


# ==========================================================
# Admin Filter
# ==========================================================

async def admin_filter(_, __, message):

    if not message.from_user:
        return False

    if message.from_user.id == OWNER_ID:
        return True

    admin = await is_admin(
        message.from_user.id
    )

    return admin is not None


admin = filters.create(admin_filter)


# ==========================================================
# Not Banned Filter
# ==========================================================

async def not_banned_filter(_, __, message):

    if not message.from_user:
        return False

    banned = await is_banned(
        message.from_user.id
    )

    return banned is None


not_banned = filters.create(not_banned_filter)


# ==========================================================
# Owner Or Admin
# ==========================================================

async def owner_or_admin_filter(_, __, message):

    if not message.from_user:
        return False

    if message.from_user.id == OWNER_ID:
        return True

    admin = await is_admin(
        message.from_user.id
    )

    return admin is not None


owner_or_admin = filters.create(
    owner_or_admin_filter
)
