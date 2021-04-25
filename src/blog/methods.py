from typing import List
from typing import Optional

from .consts import URL_API_BLOG
from .consts import URL_API_USER
from .schema import Post
from .schema import User
from .util import call_api


async def authenticate(username: str, password: str) -> Optional[User]:
    user_in = User(
        username=username,
        password=password,
    )

    data = await call_api("post", f"{URL_API_USER}/", payload=user_in)
    if not data:
        return None

    user_out = User.parse_obj(data)
    if user_out.username != username:
        return None

    return user_out


async def get_posts(blog_user_id: int) -> List[Post]:
    data = await call_api("get", f"{URL_API_BLOG}/?author_id={blog_user_id}")
    posts = []
    if isinstance(data, list):
        posts = [Post.parse_obj(chunk) for chunk in data]

    return posts
