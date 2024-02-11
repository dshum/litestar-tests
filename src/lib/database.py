from advanced_alchemy import AsyncSessionConfig
from advanced_alchemy.base import UUIDBase
from advanced_alchemy.config import EngineConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from lib import settings


class Base(UUIDBase):
    pass


db_config = SQLAlchemyAsyncConfig(
    connection_string=settings.db.URL,
    metadata=Base.metadata,
    session_config=AsyncSessionConfig(expire_on_commit=False),
    engine_config=EngineConfig(echo=settings.db.ECHO)
)

async_sessionmaker = async_sessionmaker(expire_on_commit=False)


async def on_startup() -> None:
    async with db_config.get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
