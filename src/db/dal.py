from typing import Optional

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from .models import User
from .sessions import begin_session


async def init_user(user_id: int) -> None:
    stmt = (
        insert(User)
        .values(
            {
                User.user_id: user_id,
            }
        )
        .on_conflict_do_nothing(
            index_elements=["user_id"],
        )
    )

    async with begin_session() as session:
        await session.execute(stmt)


async def get_user_auth_state(user_id: int) -> Optional[int]:
    user = await _get_user(user_id)

    return user.status if user is not None else None


async def set_user_auth_state(user_id: int, state: int) -> None:
    stmt = (
        sa.update(User)
        .where(
            User.user_id == user_id,
        )
        .values(
            {
                User.status: state,
            }
        )
    )

    async with begin_session() as session:
        await session.execute(stmt)


async def get_user_blog_username(user_id: int) -> Optional[str]:
    user = await _get_user(user_id)

    return user.blog_username if user is not None else None


async def set_user_blog_username(user_id: int, username: str) -> None:
    stmt = (
        sa.update(User)
        .where(
            User.user_id == user_id,
        )
        .values(
            {
                User.blog_username: username,
            }
        )
    )

    async with begin_session() as session:
        await session.execute(stmt)


async def reset_user_blog_auth_data(user_id: int) -> None:
    stmt = (
        sa.update(User)
        .where(
            User.user_id == user_id,
        )
        .values(
            {
                User.blog_user_id: None,
                User.blog_username: None,
                User.status: None,
            }
        )
    )

    async with begin_session() as session:
        await session.execute(stmt)


async def get_user_blog_user_id(user_id: int) -> Optional[int]:
    user = await _get_user(user_id)

    return user.blog_user_id if user is not None else None


async def set_user_blog_user_id(user_id: int, blog_user_id: int) -> None:
    stmt = (
        sa.update(User)
        .where(
            User.user_id == user_id,
        )
        .values(
            {
                User.blog_user_id: blog_user_id,
            }
        )
    )

    async with begin_session() as session:
        await session.execute(stmt)


async def _get_user(user_id: int) -> Optional[User]:
    stmt = sa.select(User).where(
        User.user_id == user_id,
    )

    async with begin_session() as session:
        response = await session.execute(stmt)
        user = response.scalars().first()

    return user
