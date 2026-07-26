from datetime import datetime


def utc_now():
    """
    Returns the current UTC datetime.
    """
    return datetime.utcnow()


def format_seconds(seconds: int) -> str:
    """
    Convert seconds into a human-readable format.
    """
    seconds = int(seconds)

    if seconds < 60:
        return f"{seconds} second(s)"

    minutes, seconds = divmod(seconds, 60)

    if minutes < 60:
        return f"{minutes} minute(s) {seconds} second(s)"

    hours, minutes = divmod(minutes, 60)

    return f"{hours} hour(s) {minutes} minute(s)"
