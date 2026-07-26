import asyncio
import importlib
import pkgutil
import traceback

import uvicorn

from config import config
from database import setup_database
from loader import app


def load_handlers():
    import handlers

    for module in pkgutil.iter_modules(handlers.__path__):
        importlib.import_module(f"handlers.{module.name}")

    print("✅ All handlers loaded")


async def run_bot():
    try:
        print("Connecting database...")
        await setup_database()
        print("✅ Database connected successfully.")

        load_handlers()

        print("Starting Telegram client...")
        await app.start()

        print("✅ Telegram client started.")

        me = await app.get_me()

        print("=" * 50)
        print(f"🤖 {me.first_name}")
        print(f"👤 @{me.username}")
        print("=" * 50)

        await app.idle()

    except Exception as e:
        print("\n" + "=" * 50)
        print("BOT START ERROR")
        print("=" * 50)
        traceback.print_exc()
        print("=" * 50)


async def run_web():
    config_uvicorn = uvicorn.Config(
        "web:app",
        host=config.HOST,
        port=config.PORT,
        log_level="info",
    )

    server = uvicorn.Server(config_uvicorn)
    await server.serve()


async def main():
    await asyncio.gather(
        run_bot(),
        run_web()
    )


if __name__ == "__main__":
    asyncio.run(main())
