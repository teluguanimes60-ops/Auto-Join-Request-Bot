from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="AutoJoinBot",
    version="1.0.0"
)


@app.get("/")
async def home():
    return JSONResponse(
        {
            "status": "running",
            "bot": "AutoJoinBot",
            "message": "Bot is online."
        }
    )


@app.get("/health")
async def health():
    return JSONResponse(
        {
            "status": "healthy"
        }
    )
