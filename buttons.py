from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==========================
# START MENU
# ==========================

def start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")
        ],
        [
            InlineKeyboardButton("📋 My Channels", callback_data="my_channels")
        ],
        [
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ])


# ==========================
# BACK BUTTON
# ==========================

def back_button(data="start"):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⬅️ Back", callback_data=data)
        ]
    ])


# ==========================
# CHANNEL SETTINGS
# ==========================

def channel_settings(channel_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⏰ Delay Time",
                callback_data=f"delay_{channel_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Welcome Message",
                callback_data=f"welcome_{channel_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🟢 Enable",
                callback_data=f"enable_{channel_id}"
            ),
            InlineKeyboardButton(
                "🔴 Disable",
                callback_data=f"disable_{channel_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 Remove Channel",
                callback_data=f"remove_{channel_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="my_channels"
            )
        ]
    ])


# ==========================
# DELAY MENU
# ==========================

def delay_buttons(channel_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "30 Seconds",
                callback_data=f"setdelay_{channel_id}_30"
            ),
            InlineKeyboardButton(
                "1 Minute",
                callback_data=f"setdelay_{channel_id}_60"
            )
        ],
        [
            InlineKeyboardButton(
                "5 Minutes",
                callback_data=f"setdelay_{channel_id}_300"
            ),
            InlineKeyboardButton(
                "10 Minutes",
                callback_data=f"setdelay_{channel_id}_600"
            )
        ],
        [
            InlineKeyboardButton(
                "30 Minutes",
                callback_data=f"setdelay_{channel_id}_1800"
            ),
            InlineKeyboardButton(
                "1 Hour",
                callback_data=f"setdelay_{channel_id}_3600"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data=f"channel_{channel_id}"
            )
        ]
    ])


# ==========================
# OWNER PANEL
# ==========================

def owner_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="stats"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="broadcast"
            )
        ],
        [
            InlineKeyboardButton(
                "👥 Users",
                callback_data="users"
            ),
            InlineKeyboardButton(
                "📺 Channels",
                callback_data="channels"
            )
        ],
        [
            InlineKeyboardButton(
                "📜 Logs",
                callback_data="logs"
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="start"
            )
        ]
    ])


# ==========================
# CONFIRM REMOVE
# ==========================

def confirm_remove(channel_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Yes",
                callback_data=f"confirmremove_{channel_id}"
            ),
            InlineKeyboardButton(
                "❌ No",
                callback_data=f"channel_{channel_id}"
            )
        ]
    ])


# ==========================
# CLOSE BUTTON
# ==========================

def close_button():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "❌ Close",
                callback_data="close"
            )
        ]
    ])

# ==========================================================
# MY CHANNELS
# ==========================================================

def my_channels_buttons(channels):

    rows = []

    for channel in channels:

        rows.append([
            InlineKeyboardButton(
                f"📺 {channel['title']}",
                callback_data=f"channel_{channel['channel_id']}"
            )
        ])

    if not rows:
        rows.append([
            InlineKeyboardButton(
                "No Channels Added",
                callback_data="ignore"
            )
        ])

    rows.append([
        InlineKeyboardButton(
            "➕ Add Channel",
            callback_data="add_channel"
        )
    ])

    rows.append([
        InlineKeyboardButton(
            "⬅️ Back",
            callback_data="start"
        )
    ])

    return InlineKeyboardMarkup(rows)


# ==========================================================
# ENABLE / DISABLE
# ==========================================================

def enable_disable_button(channel_id, enabled):

    if enabled:
        text = "🔴 Disable Auto Accept"
        callback = f"disable_{channel_id}"
    else:
        text = "🟢 Enable Auto Accept"
        callback = f"enable_{channel_id}"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text,
                callback_data=callback
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data=f"channel_{channel_id}"
            )
        ]
    ])


# ==========================================================
# IGNORE
# ==========================================================

def ignore_button():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "•",
                callback_data="ignore"
            )
        ]
    ])
