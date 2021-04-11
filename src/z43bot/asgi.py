from dotenv import load_dotenv
from fastapi import Body
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
    debug(update)
    try:
        text = update.message.text
        reply = text.capitalize() if isinstance(text, str) else "что это?"

        await telegram.send_message(
            chat_id=update.message.chat.id,
            reply_to_message_id=update.message.message_id,
            text=reply,
        )
    except Exception as err:  # pylint: disable=broad-except
        import traceback  # pylint: disable=import-outside-toplevel

        debug(err)
        debug(traceback.format_exc())

    return {"ok": True}
