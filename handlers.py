import asyncio
import logging

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    Message,
    CallbackQuery,
)

from config import OWNER_ID
from database import (
    add_user,
    add_channel,
    get_owner_channels,
    get_channel,
    get_stats
)

from buttons import (
    start_buttons,
    back_button,
    owner_buttons,
    my_channels_buttons,
    channel_settings
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# Runtime User State
# ==========================================================

USER_STATE = {}


def set_state(user_id: int, key: str, value):
    USER_STATE.setdefault(user_id, {})
    USER_STATE[user_id][key] = value


def get_state(user_id: int, key: str):
    return USER_STATE.get(user_id, {}).get(key)


def clear_state(user_id: int):
    USER_STATE.pop(user_id, None)


def is_owner(user_id: int):
    return user_id == OWNER_ID


# ==========================================================
# Helpers
# ==========================================================

async def safe_edit(message, text, reply_markup=None):
    try:
        await message.edit_text(
            text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception:
        pass


async def auto_delete(message, seconds=20):
    await asyncio.sleep(seconds)
    try:
        await message.delete()
    except Exception:
        pass


# ==========================================================
# /start
# ==========================================================

async def start_command(client: Client, message: Message):

    await add_user(message.from_user)

    text = (
        f"👋 Hello {message.from_user.mention}\n\n"
        "I'm an Auto Join Request Accepter Bot.\n\n"
        "Use the buttons below to manage your channels."
    )

    if is_owner(message.from_user.id):

        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "➕ Add Channel",
                    callback_data="add_channel"
                )
            ],
            [
                InlineKeyboardButton(
                    "📋 My Channels",
                    callback_data="my_channels"
                )
            ],
            [
                InlineKeyboardButton(
                    "👑 Owner Panel",
                    callback_data="owner_panel"
                )
            ],
            [
                InlineKeyboardButton(
                    "ℹ️ About",
                    callback_data="about"
                ),
                InlineKeyboardButton(
                    "❓ Help",
                    callback_data="help"
                )
            ]
        ])

    else:
        keyboard = start_buttons()

    await message.reply_text(
        text,
        reply_markup=keyboard
    )


# ==========================================================
# Callback Queries (Part 1)
# ==========================================================

async def callback_handler(
    client: Client,
    callback: CallbackQuery
):

    data = callback.data

    await callback.answer()

    # -------------------------
    # Home
    # -------------------------

    if data == "start":

        if is_owner(callback.from_user.id):

            from pyrogram.types import (
                InlineKeyboardMarkup,
                InlineKeyboardButton
            )

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "➕ Add Channel",
                        callback_data="add_channel"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📋 My Channels",
                        callback_data="my_channels"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👑 Owner Panel",
                        callback_data="owner_panel"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ℹ️ About",
                        callback_data="about"
                    ),
                    InlineKeyboardButton(
                        "❓ Help",
                        callback_data="help"
                    )
                ]
            ])

        else:
            keyboard = start_buttons()

        await safe_edit(
            callback.message,
            "🏠 Main Menu",
            keyboard
        )

        return

    # -------------------------
    # Help
    # -------------------------

    if data == "help":

        await safe_edit(
            callback.message,
            "❓ Help\n\n"
            "1. Add the bot as Admin.\n"
            "2. Give Manage Join Requests permission.\n"
            "3. Click Add Channel.\n"
            "4. Forward a post from your channel.\n"
            "5. Set your delay.\n",
            back_button()
        )

        return

    # -------------------------
    # About
    # -------------------------

    if data == "about":

        await safe_edit(
            callback.message,
            "🤖 Auto Join Request Bot\n\n"
            "Automatically accepts join requests "
            "after your selected delay.",
            back_button()
        )

        return

    # -------------------------
    # Owner Panel
    # -------------------------

    if data == "owner_panel":

        if not is_owner(callback.from_user.id):
            return

        stats = await get_stats()

        text = (
            "👑 Owner Panel\n\n"
            f"👥 Users : {stats['users']}\n"
            f"📺 Channels : {stats['channels']}\n"
            f"📜 Logs : {stats['logs']}"
        )

        await safe_edit(
            callback.message,
            text,
            owner_buttons()
        )

        return

    # -------------------------
    # Add Channel
    # -------------------------

    if data == "add_channel":

        set_state(
            callback.from_user.id,
            "mode",
            "waiting_channel"
        )

        await safe_edit(
            callback.message,
            "📨 Forward any message from your channel.\n\n"
            "Requirements:\n"
            "• Bot must be Admin\n"
            "• Manage Join Requests permission enabled",
            back_button()
        )

        return

    # -------------------------
    # My Channels
    # -------------------------

    if data == "my_channels":

        channels = await get_owner_channels(
            callback.from_user.id
        )

        await safe_edit(
            callback.message,
            "📋 Your Channels",
            my_channels_buttons(channels)
        )

        return

    # -------------------------
    # Open Channel Settings
    # -------------------------

    if data.startswith("channel_"):

        channel_id = int(
            data.split("_")[1]
        )

        channel = await get_channel(
            channel_id
        )

        if not channel:
            await callback.answer(
                "Channel not found.",
                show_alert=True
            )
            return

        text = (
            f"📺 {channel['title']}\n\n"
            f"Status : {'🟢 Enabled' if channel['status'] else '🔴 Disabled'}\n"
            f"Delay : {channel['delay']} seconds\n"
            f"Welcome : {'Configured' if channel['welcome'] else 'Not Configured'}"
        )

        await safe_edit(
            callback.message,
            text,
            channel_settings(channel_id)
        )

        return

    # -------------------------
    # Ignore
    # -------------------------

    if data == "ignore":
        return

# ==========================================================
# Verify Bot Permissions
# ==========================================================

async def verify_bot_permissions(
    client: Client,
    channel_id: int
):

    try:

        me = await client.get_chat_member(
            channel_id,
            "me"
        )

    except Exception:
        return False, (
            "❌ I couldn't access this channel.\n\n"
            "Please add me as an Admin first."
        )

    if me.status != ChatMemberStatus.ADMINISTRATOR:

        return False, (
            "❌ I'm not an administrator in this channel."
        )

    if not me.privileges:

        return False, (
            "❌ Administrator privileges not found."
        )

    if not me.privileges.can_manage_chat:

        return False, (
            "❌ Please enable **Manage Chat** permission."
        )

    if not me.privileges.can_invite_users:

        return False, (
            "❌ Please enable **Invite Users** permission."
        )

    return True, "OK"


# ==========================================================
# Forwarded Channel Detection
# ==========================================================

async def forwarded_channel_handler(
    client: Client,
    message: Message
):

    user_id = message.from_user.id

    if get_state(user_id, "mode") != "waiting_channel":
        return

    chat = None

    # Forwarded channel post

    if message.forward_from_chat:

        if message.forward_from_chat.type.name != "CHANNEL":
            return

        chat = message.forward_from_chat

    # Automatic Forward

    elif message.sender_chat:

        if message.sender_chat.type.name != "CHANNEL":
            return

        chat = message.sender_chat

    else:

        return

    # Already Added

    old = await get_channel(chat.id)

    if old:

        clear_state(user_id)

        await message.reply_text(
            "⚠️ This channel is already added."
        )

        return

    # Permission Check

    ok, reason = await verify_bot_permissions(
        client,
        chat.id
    )

    if not ok:

        clear_state(user_id)

        await message.reply_text(reason)

        return

    # Save temporarily

    set_state(
        user_id,
        "channel_id",
        chat.id
    )

    set_state(
        user_id,
        "channel_title",
        chat.title
    )

    set_state(
        user_id,
        "channel_username",
        chat.username
    )

    clear_state(user_id)

    await add_channel(
        owner_id=user_id,
        chat=chat
    )

    await message.reply_text(
        f"✅ Channel Added Successfully\n\n"
        f"📺 {chat.title}\n\n"
        f"Default Delay : 60 Seconds\n\n"
        "Open **My Channels** to configure it."
    )

    logger.info(
        f"Channel Added : {chat.title}"
    )

    
