from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {
        "status": "running",
        "bot": "Auto Join Request Bot"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
