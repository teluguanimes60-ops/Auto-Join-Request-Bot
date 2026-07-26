import asyncio
import importlib
import pkgutil
import uvicorn

from loader import app
from database import setup_database
from config import config


def load_handlers():
    """Automatically import all handler modules."""
    import handlers

    for module in pkgutil.iter_modules(handlers.__path__):
        importlib.import_module(f"handlers.{module.name}")

    print("✅ Handlers Loaded")


async def start_bot():
    await setup_database()

    # Load all handlers
    load_handlers()

    await app.start()

    me = await app.get_me()

    print("=" * 50)
    print(f"🤖 Bot Started Successfully")
    print(f"👤 Name : {me.first_name}")
    print(f"🔗 Username : @{me.username}")
    print(f"🆔 ID : {me.id}")
    print("=" * 50)

    await asyncio.Event().wait()


async def start_web():
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
        start_bot(),
        start_web()
    )


if __name__ == "__main__":
    asyncio.run(main())
