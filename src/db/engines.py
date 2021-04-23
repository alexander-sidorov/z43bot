from sqlalchemy.ext.asyncio import create_async_engine

from config import settings
from db.util import with_driver

engine = create_async_engine(
    with_driver(settings.database_url, "asyncpg"),
    echo=settings.debug_sql,
)
