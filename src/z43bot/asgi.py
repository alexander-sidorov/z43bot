from dotenv import load_dotenv
from fastapi import FastAPI

from z43bot import telegram
from z43bot.config import settings
from z43bot.util import debug

load_dotenv()

app = FastAPI()


@app.get("/settings/")
async def handle_settings():
    debug(settings)
    return settings


@app.post("/webhook/")
async def tg_webhook(update: telegram.Update):
    try:
        await telegram.send_message(
            chat_id=update.message.chat.id,
            text=update.message.text.capitalize(),
        )
    except Exception as err:  # pylint: disable=broad-except
        import traceback  # pylint: disable=import-outside-toplevel

        debug(err)
        debug(traceback.format_exc())

    return {"ok": True}
