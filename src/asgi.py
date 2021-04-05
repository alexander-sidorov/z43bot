import os
from typing import Optional

from fastapi import FastAPI
from pydantic import Field
from pydantic.main import BaseModel

app = FastAPI()


class ConfigParams(BaseModel):
    bot_token: Optional[str] = Field(None)
    pythonpath: Optional[str] = Field(None)


@app.get("/config/")
async def config():
    cp = ConfigParams(
        bot_token=os.getenv("BOT_TOKEN"),
        pythonpath=os.getenv("PYTHONPATH"),
    )

    return cp
