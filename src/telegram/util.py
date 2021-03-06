from typing import Optional
from typing import Type
from typing import TypeVar

import aiohttp
from aiohttp import ClientResponse
from pydantic import BaseModel
from starlette import status

from config import settings
from util import debug

from .consts import TELEGRAM_BOT_API
from .types import TelegramResponse
from .types import WebhookInfo

OutputDataT = TypeVar("OutputDataT", bound=BaseModel)


async def invoke_api_method(
    method_name: str,
    data: Optional[BaseModel],
    output_type: Optional[Type[OutputDataT]],
) -> Optional[OutputDataT]:
    """
    Generic function which invokes an arbitrary method from Telegram Bot API

    :param method_name: name of the API method
    :param data: some data for the method
    :param output_type: type of response data or None
    :return: object of output type or None
    """

    url = f"{TELEGRAM_BOT_API}/{method_name}"

    request_kw = {}

    if data is not None:
        request_kw.update(
            dict(
                json=data.dict(),
            )
        )

    async with aiohttp.ClientSession() as session:
        response_http: ClientResponse
        async with session.post(url, **request_kw) as response_http:
            payload = await response_http.json()

            if response_http.status != status.HTTP_200_OK:
                debug(response_http)
                debug(payload)
                errmsg = (
                    f"method {method_name!r}"
                    f" failed with status {response_http.status}"
                )
                raise RuntimeError(errmsg)

    response_tg = TelegramResponse.parse_obj(payload)

    if not response_tg.ok:
        debug(response_tg)
        errmsg = f"method {method_name!r} failed: {response_tg.result}"
        raise RuntimeError(errmsg)

    result = None

    if output_type is not None:
        result = output_type.parse_obj(response_tg.result)

    return result


def shadow_webhook_secret(webhook: WebhookInfo) -> WebhookInfo:
    if not webhook.url:
        return webhook

    safe_url = webhook.url.replace(settings.webhook_secret, "")
    if safe_url.endswith("//"):
        safe_url = safe_url[:-1]

    result = webhook.copy(
        update={
            "url": safe_url,
        }
    )

    return result
