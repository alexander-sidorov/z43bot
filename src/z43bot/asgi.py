from dotenv import load_dotenv
from fastapi import FastAPI

from z43bot.config import settings
from z43bot.util import debug

load_dotenv()

app = FastAPI()


@app.get("/settings/")
async def handle_settings():
    debug(settings)
    return settings
