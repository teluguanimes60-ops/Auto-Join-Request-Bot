import asyncio
import importlib
import pkgutil

import uvicorn

from config import config
from database import setup_database
from loader import app


def load_handlers():
    import handlers

    for module in pkgutil.iter_modules(handlers.__path__):
        importlib.import_module(
            f"handlers.{module.name}"
        )

    print("✅ All handlers loaded.")


async def run_bot():
    await setup_database()

    load_handlers()

    await app.start()

    me = await app.get_me()

    print("=" * 50)
    print(f"🤖 {me.first_name} Started")
    print(f"👤 @{me.username}")
    print("=" * 50)

    await asyncio.Event().wait()


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
