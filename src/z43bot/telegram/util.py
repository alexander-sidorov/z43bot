from typing import Type
from typing import TypeVar

import aiohttp
from aiohttp import ClientResponse
from pydantic.main import BaseModel
from starlette import status

from z43bot.telegram.consts import TELEGRAM_BOT_API
from z43bot.util import debug

OutputDataT = TypeVar("OutputDataT", bound=BaseModel)


async def invoke_api_method(
    method_name: str,
    data: BaseModel,
    output_type: Type[OutputDataT],
) -> OutputDataT:
    """
    Generic function which invokes an arbitrary method from Telegram Bot API

    :param method_name: name of the API method
    :param data: some data for the method
    :param output_type: type of response data
    :return: object of output type
    """

    url = f"{TELEGRAM_BOT_API}/{method_name}"

    async with aiohttp.ClientSession() as session:
        response: ClientResponse
        async with session.post(url, json=data.dict()) as response:
            payload = await response.json()

            if response.status != status.HTTP_200_OK:
                debug(response)
                debug(payload)
                errmsg = (
                    f"method {method_name!r}"
                    f" failed with status {response.status}"
                )
                raise RuntimeError(errmsg)

    result = output_type.parse_obj(payload)

    return result
