import asyncio

import sqlalchemy as sa

from db.engines import engine

migrations = [
    """
    create table if not exists users(
        id serial primary key,
        user_id integer unique,
        blog_user_id integer,
        blog_username text,
        state_auth integer
    );
    """,
]


async def apply_migrations():
    async with engine.begin() as conn:
        for migration in migrations:
            await conn.execute(sa.text(migration))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(apply_migrations())
