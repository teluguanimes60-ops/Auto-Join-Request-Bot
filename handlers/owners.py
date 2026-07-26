from pyrogram import Client
from pyrogram.types import CallbackQuery

from database import owners
from utils.permissions import is_owner
from utils.keyboards import back_button


@Client.on_callback_query()
async def owner_callbacks(client: Client, callback: CallbackQuery):

    data = callback.data

    # ===============================
    # Owner List
    # ===============================
    if data != "owners":
        return

    if not await is_owner(callback.from_user.id):
        return await callback.answer(
            "You are not authorized.",
            show_alert=True
        )

    owner_list = []

    async for owner in owners.find():
        owner_list.append(f"• `{owner['user_id']}`")

    if not owner_list:
        owner_list.append("No Owners Found.")

    text = (
        "👑 **Bot Owners**\n\n"
        + "\n".join(owner_list)
        + "\n\n"
        "More options will be added soon."
    )

    await callback.message.edit_text(
        text,
        reply_markup=back_button("owner_panel")
    )
