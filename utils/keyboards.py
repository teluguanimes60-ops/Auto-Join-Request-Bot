from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def owner_dashboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📢 Channel Manager", callback_data="channels"),
                InlineKeyboardButton("👥 Owner Manager", callback_data="owners")
            ],
            [
                InlineKeyboardButton("📊 Statistics", callback_data="stats"),
                InlineKeyboardButton("📈 Analytics", callback_data="analytics")
            ],
            [
                InlineKeyboardButton("⚙ Settings", callback_data="settings"),
                InlineKeyboardButton("🎉 Welcome", callback_data="welcome")
            ],
            [
                InlineKeyboardButton("⏳ Join Delay", callback_data="delay"),
                InlineKeyboardButton("📣 Broadcast", callback_data="broadcast")
            ],
            [
                InlineKeyboardButton("💾 Backup", callback_data="backup"),
                InlineKeyboardButton("📝 Logs", callback_data="logs")
            ],
            [
                InlineKeyboardButton("❤️ Health", callback_data="health"),
                InlineKeyboardButton("ℹ️ Bot Info", callback_data="bot_info")
            ]
        ]
    )


def user_dashboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("👤 My Profile", callback_data="profile")
            ],
            [
                InlineKeyboardButton("ℹ️ About", callback_data="about"),
                InlineKeyboardButton("🆘 Support", callback_data="support")
            ]
        ]
    )


def back_to_owner():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⬅ Back", callback_data="owner_panel")
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
