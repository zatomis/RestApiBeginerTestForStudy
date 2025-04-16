from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.DB_URL)
engine_null_pull = create_async_engine(settings.DB_URL, poolclass=NullPool)

new_async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
new_async_session_maker_null_pool = async_sessionmaker(
    bind=engine_null_pull, expire_on_commit=False
)


class BaseModelORM(DeclarativeBase):
    """
    все данные о всех моделях
    """

    pass
