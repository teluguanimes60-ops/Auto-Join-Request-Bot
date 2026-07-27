"""
User State Manager
"""

from typing import Dict, Any

# ==========================================
# In-Memory User States
# ==========================================

_user_states: Dict[int, Dict[str, Any]] = {}


# ==========================================
# Set State
# ==========================================

def set_state(user_id: int, state: str, data=None):

    _user_states[user_id] = {
        "state": state,
        "data": data
    }


# ==========================================
# Get State
# ==========================================

def get_state(user_id: int):

    return _user_states.get(user_id)


# ==========================================
# Get State Name
# ==========================================

def get_state_name(user_id: int):

    state = _user_states.get(user_id)

    if state:
        return state["state"]

    return None


# ==========================================
# Get State Data
# ==========================================

def get_state_data(user_id: int):

    state = _user_states.get(user_id)

    if state:
        return state["data"]

    return None


# ==========================================
# Clear State
# ==========================================

def clear_state(user_id: int):

    _user_states.pop(user_id, None)


# ==========================================
# Check State
# ==========================================

def has_state(user_id: int, state: str):

    current = get_state_name(user_id)

    return current == state
