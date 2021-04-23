import asyncio

import sqlalchemy as sa

from db.engines import engine

migrations = [
    """
    create table users(
        id serial primary key,
        user_id integer unique
    );
    """,
]


async def apply_migrations():
    async with engine.begin() as conn:
        for m in migrations:
            await conn.execute(sa.text(m))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(apply_migrations())
