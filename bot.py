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
        print("✅ Telegram client connected.")

        me = await app.get_me()

        print("=" * 50)
        print(f"🤖 {me.first_name} Started")
        print(f"👤 @{me.username}")
        print("=" * 50)

        await asyncio.Event().wait()

    except Exception:
        print("\n" + "=" * 50)
        print("BOT START ERROR")
        print("=" * 50)
        traceback.print_exc()
        print("=" * 50)
        raise


async def run_web():
    server = uvicorn.Server(
        uvicorn.Config(
            "web:app",
            host=config.HOST,
            port=config.PORT,
            log_level="info"
        )
    )

    await server.serve()


async def main():
    await asyncio.gather(
        run_bot(),
        run_web()
    )


if __name__ == "__main__":
    asyncio.run(main())
