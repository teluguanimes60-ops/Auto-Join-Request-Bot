from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI(
    title="Auto Join Request Bot",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "message": "🤖 Auto Join Request Bot is running!"
    }


@app.get("/health")
async def health():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "Auto Join Request Bot",
            "time": datetime.utcnow().isoformat() + "Z"
        }
    )


@app.get("/ping")
async def ping():
    return {
        "response": "pong"
    }
