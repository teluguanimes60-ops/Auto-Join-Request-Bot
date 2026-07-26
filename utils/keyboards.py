from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# ==========================
# USER DASHBOARD
# ==========================

def user_dashboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👤 My Profile",
                    callback_data="profile"
                )
            ],
            [
                InlineKeyboardButton(
                    "ℹ️ About",
                    callback_data="about"
                ),
                InlineKeyboardButton(
                    "🆘 Support",
                    callback_data="support"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )


# ==========================
# OWNER DASHBOARD
# ==========================

def owner_dashboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 Channels",
                    callback_data="channels"
                ),
                InlineKeyboardButton(
                    "👑 Owners",
                    callback_data="owners"
                )
            ],
            [
                InlineKeyboardButton(
                    "📊 Statistics",
                    callback_data="stats"
                ),
                InlineKeyboardButton(
                    "🤖 Bot Info",
                    callback_data="bot_info"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 User Panel",
                    callback_data="user_dashboard"
                ),
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )


# ==========================
# BACK BUTTON
# ==========================

def back_button(callback="owner_panel"):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data=callback
                )
            ]
        ]
    )


# ==========================
# CLOSE BUTTON
# ==========================

def close_button():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )


# ==========================
# CHANNEL PANEL
# ==========================

def channel_panel():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Channel Guide",
                    callback_data="add_channel"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="owner_panel"
                )
            ]
        ]
    )


# ==========================
# CONFIRM BUTTONS
# ==========================

def confirm_buttons(
    yes="confirm_yes",
    no="confirm_no"
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Yes",
                    callback_data=yes
                ),
                InlineKeyboardButton(
                    "❌ No",
                    callback_data=no
                )
            ]
        ]
    )
