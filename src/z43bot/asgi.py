from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Form
from fastapi import HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from z43bot import telegram
from z43bot.config import settings
from z43bot.dirs import DIR_TEMPLATES
from z43bot.util import debug

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory=DIR_TEMPLATES.as_posix())


@app.get("/", response_class=HTMLResponse)
async def handle_index(
    request: Request,
):
    webhook = await telegram.get_webhook_info()
    debug(webhook)

    context = {
        "url_webhook_current": webhook.url,
        "url_webhook_new": f"{settings.service_url}/webhook/",
    }

    response = templates.TemplateResponse(
        "index.html", {"request": request, **context}
    )

    return response


@app.post("/webhook-setup/")
async def handle_setup_webhook(
    password: str = Form(...),
):
    if password != settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin is allowed to configure webhook",
        )

    new_webhook_url = f"{settings.service_url}/webhook/"

    await telegram.set_webhook(url=new_webhook_url)

    return RedirectResponse(
        "/",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@app.post("/webhook/")
async def handle_webhook(update: telegram.Update):
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
