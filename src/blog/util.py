from typing import Optional
from typing import TypeVar

import aiohttp
from aiohttp import ClientResponse
from pydantic.main import BaseModel
from starlette import status

from .consts import CONTENT_TYPE

T = TypeVar("T", bound=BaseModel)


async def call_api(
    method: str,
    url: str,
    *,
    payload: Optional[BaseModel] = None,
    success_status: int = status.HTTP_200_OK,
) -> Optional[T]:
    headers = {
        "Content-Type": CONTENT_TYPE,
    }

    request_kw = {}

    if payload:
        request_kw["json"] = payload.dict(exclude_unset=True)

    async with aiohttp.ClientSession(headers=headers) as session:
        response: ClientResponse

        method_ = getattr(session, method)

        response = await method_(
            url,
            **request_kw,
        )

        if response.status != success_status:
            return None

        data = await response.json()
        if not data.get("meta", {}).get("ok"):
            return None

        data = data["data"]

        return data
