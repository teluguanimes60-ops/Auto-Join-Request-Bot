from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def owner_dashboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📢 Channels", callback_data="channels"),
                InlineKeyboardButton("👥 Owners", callback_data="owners")
            ],
            [
                InlineKeyboardButton("📊 Statistics", callback_data="stats"),
                InlineKeyboardButton("📣 Broadcast", callback_data="broadcast")
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
                InlineKeyboardButton("🗄 Backup", callback_data="backup")
            ],
            [
                InlineKeyboardButton("📝 Logs", callback_data="logs"),
                InlineKeyboardButton("ℹ️ Bot Info", callback_data="bot_info")
            ]
        ]
    )


def user_dashboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👤 My Profile", callback_data="profile"),
                InlineKeyboardButton("📋 My Requests", callback_data="my_requests")
            ],
            [
                InlineKeyboardButton("✅ Joined Channels", callback_data="joined_channels")
            ],
            [
                InlineKeyboardButton("🆘 Support", callback_data="support"),
                InlineKeyboardButton("ℹ️ About", callback_data="about")
            ]
        ]
    )


def back_button(data="home"):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⬅️ Back", callback_data=data)
            ]
        ]
    )


def close_button():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("❌ Close", callback_data="close")
            ]
        ]
    )


def yes_no(confirm_data, cancel_data):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✅ Yes", callback_data=confirm_data),
                InlineKeyboardButton("❌ No", callback_data=cancel_data)
            ]
        ]
    )
