from config import LOG_CHANNEL

# ==========================================================
# Send Log
# ==========================================================

async def send_log(client, text):

    if not LOG_CHANNEL:
        return

    try:

        await client.send_message(
            chat_id=int(LOG_CHANNEL),
            text=text,
            disable_web_page_preview=True
        )

    except Exception as e:
        print(f"Log Error: {e}")


# ==========================================================
# User Log
# ==========================================================

async def log_user(client, user, action):

    text = (
        "👤 User Activity\n\n"
        f"Action : {action}\n"
        f"Name : {user.first_name}\n"
        f"ID : `{user.id}`\n"
    )

    if user.username:
        text += f"Username : @{user.username}"

    await send_log(client, text)


# ==========================================================
# Channel Log
# ==========================================================

async def log_channel(client, channel, action):

    text = (
        "📢 Channel Activity\n\n"
        f"Action : {action}\n"
        f"Title : {channel.title}\n"
        f"ID : `{channel.id}`\n"
    )

    if channel.username:
        text += f"Username : @{channel.username}"

    await send_log(client, text)


# ==========================================================
# Join Request Log
# ==========================================================

async def log_join(client, channel, user):

    text = (
        "✅ Join Request Accepted\n\n"
        f"Channel : {channel.title}\n"
        f"User : {user.first_name}\n"
        f"User ID : `{user.id}`"
    )

    await send_log(client, text)


# ==========================================================
# Error Log
# ==========================================================

async def log_error(client, error):

    text = (
        "❌ Bot Error\n\n"
        f"`{error}`"
    )

    await send_log(client, text)
