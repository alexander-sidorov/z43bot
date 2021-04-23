from typing import List
from typing import Optional

import aiohttp
from aiohttp import ClientResponse
from starlette import status

from .consts import CONTENT_TYPE
from .consts import URL_API_BLOG
from .consts import URL_API_USER
from .schema import Post
from .schema import User


async def authenticate(username: str, password: str) -> Optional[int]:
    user_in = User(
        username=username,
        password=password,
    )

    async with aiohttp.ClientSession() as session:
        response: ClientResponse
        response = await session.post(
            f"{URL_API_USER}/",
            json=user_in.dict(exclude_unset=True),
            headers={
                "Content-Type": CONTENT_TYPE,
            },
        )
        if response.status != status.HTTP_200_OK:
            return None

        payload: dict = await response.json()
        if not payload["meta"]["ok"]:
            return None

    user_out = User.parse_obj(payload["data"])
    if user_out.username != username:
        return None

    return user_out.id


async def get_posts(blog_user_id: int) -> List[Post]:
    all_posts = await get_all_posts()
    user_posts = [post for post in all_posts if post.author_id == blog_user_id]
    return user_posts


async def get_all_posts() -> List[Post]:
    async with aiohttp.ClientSession() as session:
        response: ClientResponse
        response = await session.get(
            f"{URL_API_BLOG}/",
            headers={
                "Content-Type": CONTENT_TYPE,
            },
        )
        assert response.status == status.HTTP_200_OK

        payload: dict = await response.json()
        assert payload["meta"]["ok"]

    posts = [Post.parse_obj(post) for post in payload["data"]]

    return posts
