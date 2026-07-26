from database import owners


async def is_owner(user_id: int) -> bool:
    """
    Returns True if the user is an owner.
    """
    owner = await owners.find_one(
        {"user_id": user_id}
    )
    return owner is not None


async def require_owner(user_id: int):
    """
    Alias for future expansion.
    """
    return await is_owner(user_id)
