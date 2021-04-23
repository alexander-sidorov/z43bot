import dataclasses
import enum
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


_automata = {}


def register_state_handler(*states: AuthState):
    def register_decorator(handler: Callable):
        global _automata
        _automata.update({state: handler for state in states})
        return handler

    return register_decorator


async def process(update: Update) -> str:
    user_id = update.message.from_.id

    await dal.init_user(user_id)

    state = await get_state(user_id)
    handler = get_handler(state)
    next_ = await handler(update)
    await set_state(user_id, next_.state)

    return next_.signal


def get_handler(state: AuthState) -> Callable:
    handler = _automata[state]

    return handler


async def get_state(user_id: int) -> AuthState:
    state_value = await dal.get_user_auth_state(user_id)

    try:
        state = AuthState(state_value)
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
    user_id = update.message.from_.id
    username = update.message.text

    await dal.set_user_blog_username(user_id, username)

    return Next(
        signal="Отлично. Теперь напиши пароль. Мы его не сохраняем, честно!",
        state=AuthState.WAITING_FOR_PASSWORD,
    )


@register_state_handler(AuthState.WAITING_FOR_PASSWORD)
async def _process_password(update: Update) -> Next:
    user_id = update.message.from_.id
    password = update.message.text
    username = await dal.get_user_blog_username(user_id)

    blog_user_id = await blog.authenticate(username, password)

    if not blog_user_id:
        await dal.reset_user_blog_auth_data(user_id)

        return Next(
            signal=(
                "Аутентификация провалена.\n"
                "Попробуем ещё раз.\n"
                "Пришли, пож, свой юзернейм в Блоге."
            ),
            state=AuthState.WAITING_FOR_USERNAME,
        )

    await dal.set_user_blog_user_id(user_id, blog_user_id)

    posts = await blog.get_posts(blog_user_id)
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
