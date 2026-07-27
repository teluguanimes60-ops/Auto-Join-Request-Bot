from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database.models import (
    get_channel,
    update_channel_setting,
)


# ==========================================
# Channel Settings Panel
# ==========================================

@Client.on_callback_query()
async def settings_callbacks(client: Client, query: CallbackQuery):

    data = query.data

    # callback_data format:
    # settings_<channel_id>

    if data.startswith("settings_"):

        channel_id = int(data.split("_")[1])

        channel = await get_channel(channel_id)

        if not channel:
            return await query.answer(
                "Channel not found.",
                show_alert=True
            )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    f"✅ Auto Accept : {'ON' if channel.get('auto_accept', True) else 'OFF'}",
                    callback_data=f"toggle_auto_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    f"💬 Welcome : {'ON' if channel.get('welcome', True) else 'OFF'}",
                    callback_data=f"toggle_welcome_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    f"🗑 Auto Delete : {'ON' if channel.get('auto_delete', False) else 'OFF'}",
                    callback_data=f"toggle_delete_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "📝 Custom Welcome",
                    callback_data=f"custom_welcome_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "⏱ Delete Timer",
                    callback_data=f"delete_timer_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "📊 Join Logs",
                    callback_data=f"toggle_logs_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="my_channels"
                )
            ]
        ])

        return await query.message.edit_text(
            f"⚙ **Settings**\n\n{channel['title']}",
            reply_markup=keyboard
        )


# ==========================================
# Toggle Auto Accept
# ==========================================

    elif data.startswith("toggle_auto_"):

        channel_id = int(data.split("_")[2])

        channel = await get_channel(channel_id)

        value = not channel.get("auto_accept", True)

        await update_channel_setting(
            channel_id,
            "auto_accept",
            value
        )

        return await query.answer(
            f"Auto Accept {'Enabled' if value else 'Disabled'}"
        )


# ==========================================
# Toggle Welcome
# ==========================================

    elif data.startswith("toggle_welcome_"):

        channel_id = int(data.split("_")[2])

        channel = await get_channel(channel_id)

        value = not channel.get("welcome", True)

        await update_channel_setting(
            channel_id,
            "welcome",
            value
        )

        return await query.answer(
            f"Welcome Message {'Enabled' if value else 'Disabled'}"
        )


# ==========================================
# Toggle Auto Delete
# ==========================================

    elif data.startswith("toggle_delete_"):

        channel_id = int(data.split("_")[2])

        channel = await get_channel(channel_id)

        value = not channel.get("auto_delete", False)

        await update_channel_setting(
            channel_id,
            "auto_delete",
            value
        )

        return await query.answer(
            f"Auto Delete {'Enabled' if value else 'Disabled'}"
        )


# ==========================================
# Delete Timer
# ==========================================

    elif data.startswith("delete_timer_"):

        channel_id = int(data.split("_")[2])

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "10 Seconds",
                    callback_data=f"timer_10_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "30 Seconds",
                    callback_data=f"timer_30_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "1 Minute",
                    callback_data=f"timer_60_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "5 Minutes",
                    callback_data=f"timer_300_{channel_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "Never Delete",
                    callback_data=f"timer_0_{channel_id}"
                )
            ]
        ])

        return await query.message.edit_reply_markup(
            reply_markup=keyboard
        )


# ==========================================
# Save Delete Timer
# ==========================================

    elif data.startswith("timer_"):

        _, seconds, channel_id = data.split("_")

        await update_channel_setting(
            int(channel_id),
            "delete_time",
            int(seconds)
        )

        return await query.answer(
            "Delete timer updated."
        )


# ==========================================
# Placeholder
# ==========================================

    elif data.startswith("custom_welcome_"):

        return await query.answer(
            "Custom Welcome Message will be added in the next update.",
            show_alert=True
        )

    elif data.startswith("toggle_logs_"):

        return await query.answer(
            "Join Logs feature coming soon.",
            show_alert=True
        )
