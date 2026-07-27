from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


@Client.on_callback_query()
async def help_callback(client: Client, query: CallbackQuery):

    if query.data != "help":
        return

    text = """
❓ **Help**

### How to use

**1️⃣ Add the bot to your channel**

• Add this bot as an Administrator.

Required permissions:

✅ Invite Users
✅ Manage Join Requests
✅ Delete Messages (optional)

---

**2️⃣ Add your channel**

Press

➕ Add Channel

Send the Channel Username or Channel ID.

---

**3️⃣ Enable Auto Accept**

Open

📂 My Channels

Select your channel

Press

✅ Auto Accept

Now every join request will be accepted automatically.

---

### Optional Features

💬 Welcome Message

Send a welcome message after approval.

🗑 Auto Delete

Automatically delete the welcome message after a selected time.

⏱ Delete Timer

Choose how long the welcome message remains visible.

---

### Owner Commands

/owner

Shows the Owner Panel.

---

Need more help?

Contact the bot owner.
"""

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ℹ About",
                    callback_data="about"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Back",
                    callback_data="home"
                )
            ]
        ]
    )

    await query.message.edit_text(
        text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
