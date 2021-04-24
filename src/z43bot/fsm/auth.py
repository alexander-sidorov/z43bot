import dataclasses
import enum
from collections import Coroutine
from typing import Callable

import blog
from db import dal
from telegram import Update


@enum.unique
class AuthState(enum.Enum):
    UNKNOWN = None
    NOT_AUTHENTICATED = 1
    WAITING_FOR_USERNAME = 2
    WAITING_FOR_PASSWORD = 4
    AUTHENTICATED = 8


@dataclasses.dataclass
class Next:
    signal: str = "хз, что это"
    state: AuthState = AuthState.UNKNOWN


_AUTOMATA = {}

HandlerT = Callable[[Update], Coroutine[None, None, Next]]


def register_state_handler(*states: AuthState):
    def register_decorator(handler: HandlerT):
        global _AUTOMATA  # pylint: disable=W0603 (global-statement)
        _AUTOMATA.update({state: handler for state in states})
        return handler

    return register_decorator


async def process(update: Update) -> str:
    assert update.message.from_
    user_id = update.message.from_.id

    await dal.init_user(user_id)

    state = await get_state(user_id)
    handler = get_handler(state)
    next_ = await handler(update)
    await set_state(user_id, next_.state)

    return next_.signal


def get_handler(state: AuthState) -> HandlerT:
    handler = _AUTOMATA[state]

    return handler


async def get_state(user_id: int) -> AuthState:
    user = await dal.get_user(user_id)
    if not user:
        return AuthState.UNKNOWN

    try:
        state = AuthState(user.state_auth)
    except ValueError:
        state = AuthState.UNKNOWN

    return state


async def set_state(user_id: int, state: AuthState) -> None:
    await dal.set_user_auth_state(user_id, state.value)


@register_state_handler(AuthState.NOT_AUTHENTICATED, AuthState.UNKNOWN)
async def _handle_not_authenticated(_update: Update) -> Next:
    return Next(
        signal="Напиши свой логин/юзернейм в Блоге",
        state=AuthState.WAITING_FOR_USERNAME,
    )


@register_state_handler(AuthState.WAITING_FOR_USERNAME)
async def _handle_username(update: Update) -> Next:
    assert update.message.from_

    user_id = update.message.from_.id
    username = update.message.text

    await dal.set_user_blog_username(user_id, username)

    return Next(
        signal="Отлично. Теперь напиши пароль. Мы его не сохраняем, честно!",
        state=AuthState.WAITING_FOR_PASSWORD,
    )


@register_state_handler(AuthState.WAITING_FOR_PASSWORD)
async def _process_password(update: Update) -> Next:
    assert update.message.from_
    user_id = update.message.from_.id
    password = update.message.text
    user = await dal.get_user(user_id)

    blog_user = None
    if user and user.blog_username and password:
        blog_user = await blog.authenticate(user.blog_username, password)

    if not blog_user or not blog_user.id:
        await dal.reset_user_blog_auth_data(user_id)

        return Next(
            signal=(
                "Аутентификация провалена.\n"
                "Попробуем ещё раз.\n"
                "Пришли, пож, свой юзернейм в Блоге."
            ),
            state=AuthState.WAITING_FOR_USERNAME,
        )

    await dal.set_user_blog_user_id(user_id, blog_user.id)

    posts = await blog.get_posts(blog_user.id)
    signal = ", ".join(str(post.id) for post in posts)

    return Next(
        signal=f"Тебя узнали! Твои посты: {signal}",
        state=AuthState.AUTHENTICATED,
    )


@register_state_handler(AuthState.AUTHENTICATED)
async def _process_authenticated(update: Update) -> Next:
    return Next(
        signal=(
            f"Всё хорошо, ты заутентифицирован!\n"
            f"Твоё сообщение:\n\n"
            f"<pre>{update.json()}</pre>"
        ),
        state=AuthState.AUTHENTICATED,
    )
