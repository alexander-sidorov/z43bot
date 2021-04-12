import enum
from contextlib import closing
from typing import Optional

import asyncpg
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Form
from fastapi import HTTPException
from fastapi import Path
from pydantic import BaseModel
from pydantic import Field
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


@enum.unique
class UserStatus(enum.Enum):
    INITIAL =1
    WAITING_FOR_USERNAME = 2
    WAITING_FOR_PASSWORD = 3


@app.post("/webhook/")
async def handle_webhook(update: telegram.Update):
    debug(update)
    try:
        user: User2 = await get_or_create_user(update.message.from_.id)
        if user.blog_user_id:
            await telegram.send_message(
                chat_id=update.message.chat.id,
                reply_to_message_id=update.message.message_id,
                text=f"ТЫ: {user}, пишешь какую-то дичь: {update.message.text}",
            )
        else:
            if user.status == UserStatus.INITIAL.value:
                await ask_for_username(update.message.chat.id)
            elif user.status == UserStatus.WAITING_FOR_USERNAME.value:
                await setup_username(update.message.from_.id, update.message.text)
                await ask_for_password(update.message.chat.id)
            elif user.status == UserStatus.WAITING_FOR_PASSWORD.value:
                password = update.message.text
                await auth_on_blog(user.blog_username, password)
            else:
                raise RuntimeError(f"unknown status: {user.status}")

    except Exception as err:  # pylint: disable=broad-except
        import traceback  # pylint: disable=import-outside-toplevel

        debug(err)
        debug(traceback.format_exc())

    return {"ok": True}


class User2(BaseModel):
    id: int
    user_id: int
    blog_user_id: Optional[int] = Field(None)
    blog_username: Optional[str] = Field(None)
    status: int = Field(...)


@app.post("/xxx/{user_id}/")
async def xxx(user_id: int = Path(...)):
    conn = await asyncpg.connect(dsn=settings.database_url)
    try:
        values = await conn.fetch(
            'select * from users where id = $1',
            user_id,
        )
        debug(values)

        values2 = [
            User2.parse_obj(obj)
            for obj in values
        ]

        return values2
    finally:
        await conn.close()
