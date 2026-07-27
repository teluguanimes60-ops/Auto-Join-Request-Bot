from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import OWNER_ID
from database.models import (
    is_admin,
    get_stats,
)


# ==========================================
# Owner Panel
# ==========================================

@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):

    data = query.data
    user = query.from_user

    # ------------------------------
    # Add Channel
    # ------------------------------
    if data == "add_channel":

        text = (
            "➕ **Add Channel**\n\n"
            "1. Add this bot as Administrator.\n"
            "2. Give **Manage Join Requests** permission.\n"
            "3. Forward any message from your channel.\n\n"
            "The bot will automatically detect the channel."
        )

        return await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⬅ Back",
                            callback_data="home",
                        )
                    ]
                ]
            )
        )

    # ------------------------------
    # My Channels
    # ------------------------------
    elif data == "my_channels":

        return await query.message.edit_text(
            "📂 Your channels will appear here.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⬅ Back",
                            callback_data="home",
                        )
                    ]
                ]
            )
        )

    # ------------------------------
    # Settings
    # ------------------------------
    elif data == "settings":

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Auto Accept",
                        callback_data="auto_accept",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 Welcome Message",
                        callback_data="welcome",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Auto Delete",
                        callback_data="auto_delete",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="home",
                    )
                ],
            ]
        )

        return await query.message.edit_text(
            "⚙ **Settings Panel**",
            reply_markup=keyboard,
        )

    # ------------------------------
    # Statistics
    # ------------------------------
    elif data == "stats":

        stats = await get_stats()

        text = (
            "📊 **Bot Statistics**\n\n"
            f"👥 Users : {stats['users']}\n"
            f"🛡 Admins : {stats['admins']}\n"
            f"📂 Channels : {stats['channels']}\n"
            f"✅ Accepted Joins : {stats['joins']}"
        )

        return await query.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⬅ Back",
                            callback_data="home",
                        )
                    ]
                ]
            )
        )

    # ------------------------------
    # Help
    # ------------------------------
    elif data == "help":

        return await query.message.edit_text(
            "ℹ **Help**\n\n"
            "• Add the bot to your channel.\n"
            "• Give Manage Join Requests permission.\n"
            "• Enable Auto Accept.\n"
            "• Done ✅",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⬅ Back",
                            callback_data="home",
                        )
                    ]
                ]
            )
        )

    # ------------------------------
    # Owner Panel
    # ------------------------------
    elif data == "owner_panel":

        if user.id != OWNER_ID:
            return await query.answer(
                "This panel is only for the owner.",
                show_alert=True,
            )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👥 Users",
                        callback_data="owner_users",
                    ),
                    InlineKeyboardButton(
                        "📊 Stats",
                        callback_data="stats",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🛡 Admins",
                        callback_data="owner_admins",
                    ),
                    InlineKeyboardButton(
                        "📢 Broadcast",
                        callback_data="broadcast",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "⚙ Settings",
                        callback_data="owner_settings",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="home",
                    )
                ],
            ]
        )

        return await query.message.edit_text(
            "👑 **Owner Panel**",
            reply_markup=keyboard,
        )

    # ------------------------------
    # Admin Panel
    # ------------------------------
    elif data == "admin_panel":

        if not await is_admin(user.id):
            return await query.answer(
                "Admins only.",
                show_alert=True,
            )

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📂 Channels",
                        callback_data="my_channels",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📊 Statistics",
                        callback_data="stats",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅ Back",
                        callback_data="home",
                    )
                ],
            ]
        )

        return await query.message.edit_text(
            "🛡 **Admin Panel**",
            reply_markup=keyboard,
        )

    # ------------------------------
    # Home
    # ------------------------------
    elif data == "home":

        await query.message.delete()

        return await client.send_message(
            query.from_user.id,
            "/start"
        )

    # ------------------------------
    # Unknown Callback
    # ------------------------------
    else:
        return await query.answer(
            "Unknown button.",
            show_alert=False,
        )
