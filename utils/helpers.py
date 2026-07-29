from datetime import timedelta


# ==========================================================
# Format Seconds
# ==========================================================

def format_time(seconds: int) -> str:
    """
    Convert seconds into a readable format.
    """

    seconds = int(seconds)

    if seconds < 60:
        return f"{seconds} sec"

    if seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes} min {secs} sec"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    return f"{hours} hr {minutes} min"


# ==========================================================
# Escape Markdown
# ==========================================================

def escape_markdown(text: str) -> str:

    if not text:
        return ""

    chars = r"_*[]()~`>#+-=|{}.!"

    for ch in chars:
        text = text.replace(ch, "\\" + ch)

    return text


# ==========================================================
# Safe Mention
# ==========================================================

def mention(user):

    if user.username:
        return f"@{user.username}"

    return user.mention


# ==========================================================
# Human Number
# ==========================================================

def human_number(number: int):

    number = int(number)

    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"

    if number >= 1_000:
        return f"{number / 1_000:.1f}K"

    return str(number)


# ==========================================================
# Bool Emoji
# ==========================================================

def bool_emoji(value: bool):

    return "✅ Enabled" if value else "❌ Disabled"
