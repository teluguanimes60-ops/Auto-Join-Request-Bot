from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==========================================================
# START MENU
# ==========================================================

def start_buttons(is_owner=False):

    rows = [
        [
            InlineKeyboardButton(
                "➕ Add Channel",
                callback_data="add_channel"
            )
        ],
        [
            InlineKeyboardButton(
                "📂 My Channels",
                callback_data="my_channels"
            )
        ],
        [
            InlineKeyboardButton(
                "⚙ Settings",
                callback_data="settings"
            ),
            InlineKeyboardButton(
                "❓ Help",
                callback_data="help"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ About",
                callback_data="about"
            )
        ]
    ]

    if is_owner:
        rows.append([
            InlineKeyboardButton(
                "👑 Owner Panel",
                callback_data="owner_panel"
            )
        ])

    return InlineKeyboardMarkup(rows)


# ==========================================================
# BACK BUTTON
# ==========================================================

def back_button(data="home"):

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⬅ Back",
                callback_data=data
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
                f"📢 {channel['title']}",
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
            "⬅ Back",
            callback_data="home"
        )
    ])

    return InlineKeyboardMarkup(rows)


# ==========================================================
# CHANNEL SETTINGS
# ==========================================================

def channel_settings(channel_id):

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "✅ Auto Accept",
                callback_data=f"toggle_auto_{channel_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "💬 Welcome Message",
                callback_data=f"toggle_welcome_{channel_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "🗑 Auto Delete",
                callback_data=f"toggle_delete_{channel_id}"
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
                "📝 Custom Welcome",
                callback_data=f"custom_welcome_{channel_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "❌ Remove Channel",
                callback_data=f"remove_{channel_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="my_channels"
            )
        ]
    ])


# ==========================================================
# DELETE TIMER
# ==========================================================

def delete_timer_buttons(channel_id):

    return InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "10 Sec",
                callback_data=f"timer_10_{channel_id}"
            ),
            InlineKeyboardButton(
                "30 Sec",
                callback_data=f"timer_30_{channel_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "1 Min",
                callback_data=f"timer_60_{channel_id}"
            ),
            InlineKeyboardButton(
                "5 Min",
                callback_data=f"timer_300_{channel_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "Never",
                callback_data=f"timer_0_{channel_id}"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ Back",
                callback_data=f"channel_{channel_id}"
            )
        ]
    ])


# ==========================================================
# OWNER PANEL
# ==========================================================

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
                "👥 Users",
                callback_data="users"
            ),
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="broadcast"
            )
        ],

        [
            InlineKeyboardButton(
                "📂 Channels",
                callback_data="channels"
            ),
            InlineKeyboardButton(
                "🛡 Admins",
                callback_data="admins"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙ Bot Settings",
                callback_data="owner_settings"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅ Back",
                callback_data="home"
            )
        ]
    ])


# ==========================================================
# CONFIRM REMOVE
# ==========================================================

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
                "⬅ Back",
                callback_data=f"channel_{channel_id}"
            )
        ]
    ])


# ==========================================================
# CLOSE BUTTON
# ==========================================================

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
# IGNORE BUTTON
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
