from pyrogram import filters

from config import OWNER_ID
from database.models import (
    is_admin,
    is_banned,
    get_channel,
)


# =====================================================
# Owner Filter
# =====================================================

async def owner_filter(_, __, message):
    return (
        message.from_user is not None
        and message.from_user.id == OWNER_ID
    )


OwnerFilter = filters.create(owner_filter)


# =====================================================
# Admin Filter
# =====================================================

async def admin_filter(_, __, message):

    if message.from_user is None:
        return False

    if message.from_user.id == OWNER_ID:
        return True

    return await is_admin(message.from_user.id)


AdminFilter = filters.create(admin_filter)


# =====================================================
# Not Banned Filter
# =====================================================

async def not_banned_filter(_, __, message):

    if message.from_user is None:
        return False

    banned = await is_banned(message.from_user.id)

    return not banned


NotBannedFilter = filters.create(not_banned_filter)


# =====================================================
# Registered Channel Filter
# =====================================================

async def registered_channel_filter(_, __, update):

    try:
        chat = update.chat
    except Exception:
        return False

    if chat is None:
        return False

    channel = await get_channel(chat.id)

    return channel is not None


RegisteredChannelFilter = filters.create(
    registered_channel_filter
)


# =====================================================
# Channel Owner Filter
# =====================================================

async def channel_owner_filter(_, __, message):

    if message.from_user is None:
        return False

    if len(message.command) < 2:
        return False

    try:
        channel_id = int(message.command[1])
    except ValueError:
        return False

    channel = await get_channel(channel_id)

    if not channel:
        return False

    return channel.get("owner_id") == message.from_user.id


ChannelOwnerFilter = filters.create(
    channel_owner_filter
)


# =====================================================
# Private Chat Filter
# =====================================================

PrivateFilter = filters.private


# =====================================================
# Group Filter
# =====================================================

GroupFilter = filters.group


# =====================================================
# Channel Filter
# =====================================================

ChannelFilter = filters.channel


# =====================================================
# Bot Admin Filter
# =====================================================

async def bot_admin_filter(_, client, message):

    try:

        me = await client.get_me()

        member = await client.get_chat_member(
            message.chat.id,
            me.id
        )

        return member.status.name == "ADMINISTRATOR"

    except Exception:
        return False


BotAdminFilter = filters.create(bot_admin_filter)


# =====================================================
# Callback Owner Filter
# =====================================================

async def callback_owner_filter(_, __, query):

    return query.from_user.id == OWNER_ID


CallbackOwnerFilter = filters.create(
    callback_owner_filter
)


# =====================================================
# Callback Admin Filter
# =====================================================

async def callback_admin_filter(_, __, query):

    if query.from_user.id == OWNER_ID:
        return True

    return await is_admin(query.from_user.id)


CallbackAdminFilter = filters.create(
    callback_admin_filter
)
