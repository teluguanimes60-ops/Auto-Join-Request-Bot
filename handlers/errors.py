import logging
import traceback
from pyrogram import Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

logger = logging.getLogger(__name__)


async def error_handler(_, update, exception):
    logger.error(
        "\n========== BOT ERROR ==========\n"
        f"{traceback.format_exc()}\n"
        "==============================="
    )
    return True


def register_error_handler(app: Client):
    app.add_handler(
        MessageHandler(lambda *_: None),
        group=999
    )

    app.add_handler(
        CallbackQueryHandler(lambda *_: None),
        group=999
    )
