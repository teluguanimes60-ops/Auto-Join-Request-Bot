import asyncio
import importlib
import pkgutil

import uvicorn
from pyrogram import idle

from config import config
from database import setup_database
from loader import app


def load_handlers():
    import handlers

    for module in pkgutil.iter_modules(handlers.__path__):
        importlib.import_module(f"handlers.{module.name}")

    print("✅ All handlers loaded")


async def start_bot():
    await setup_database()

    load_handlers()

    await app.start()

    me = await app.get_me()

    print("=" * 50)
    print(f"🤖 {me.first_name}")
    print(f"👤 @{me.username}")
    print("✅ Bot Started Successfully")
    print("=" * 50)

    await idle()

    await app.stop()


async def start_web():
    server = uvicorn.Server(
        uvicorn.Config(
            app="web:app",
            host=config.HOST,
            port=config.PORT,
            log_level="info",
        )
    )

    await server.serve()


async def main():
    await asyncio.gather(
        start_bot(),
        start_web()
    )


if __name__ == "__main__":
    asyncio.run(main())
