import asyncio
import uvicorn

from loader import app
from database import setup_database
from config import config


async def start_bot():
    """Start the Telegram bot."""
    await setup_database()

    await app.start()

    me = await app.get_me()

    print("=" * 50)
    print(f"✅ {me.first_name} Started Successfully")
    print(f"🤖 Username : @{me.username}")
    print(f"🆔 Bot ID   : {me.id}")
    print("=" * 50)

    await asyncio.Event().wait()


async def start_web():
    """Start the FastAPI server for Render."""
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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
