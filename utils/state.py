"""
State Manager
Stores temporary user states in memory.
"""

USER_STATES = {}


# ==========================================================
# Set State
# ==========================================================

def set_state(user_id: int, state: str, data=None):
    USER_STATES[user_id] = {
        "state": state,
        "data": data or {}
    }


# ==========================================================
# Get State
# ==========================================================

def get_state(user_id: int):
    state = USER_STATES.get(user_id)

    if not state:
        return None

    return state["state"]


# ==========================================================
# Get State Data
# ==========================================================

def get_state_data(user_id: int):
    state = USER_STATES.get(user_id)

    if not state:
        return {}

    return state["data"]


# ==========================================================
# Has State
# ==========================================================

def has_state(user_id: int):
    return user_id in USER_STATES


# ==========================================================
# Clear State
# ==========================================================

def clear_state(user_id: int):
    USER_STATES.pop(user_id, None)


# ==========================================================
# Update State Data
# ==========================================================

def update_state_data(user_id: int, **kwargs):
    if user_id not in USER_STATES:
        return

    USER_STATES[user_id]["data"].update(kwargs)
