from fastapi import FastAPI

app = FastAPI(
    title="Auto Join Request Bot",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "status": "online",
        "bot": "Auto Join Request Bot"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "Bot is running"
    }


@app.get("/ping")
async def ping():
    return {
        "ping": "pong"
    }
