from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from .settings import settings


class Database:
    _instance = None
    _engine = None
    _async_session = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def init_engine(self):
        if self._engine is None:
            self._engine = create_async_engine(
                settings.SQLALCHEMY_DATABASE_URI,
                pool_pre_ping=settings.POOL_PRE_PING,
                pool_size=settings.POOL_SIZE,
                echo=settings.ECHO_POOL,
                max_overflow=settings.MAX_OVERFLOW,
                pool_recycle=settings.POOL_RECYCLE_IN_SECONDS,
                echo_pool=settings.ECHO_POOL,
                pool_reset_on_return=settings.POOL_RESET_ON_RETURN,
                pool_timeout=settings.POOL_TIMEOUT_IN_SECONDS,
            )
            self._async_session = sessionmaker(
                self._engine, class_=AsyncSession, expire_on_commit=False
            )

    @property
    def async_session(self):
        if self._async_session is None:
            self.init_engine()
        return self._async_session

    @property
    def engine(self):
        if self._engine is None:
            self.init_engine()
        return self._engine

    @staticmethod
    @asynccontextmanager
    async def get_db_session():
        """Gets a session from database

        Yields:
            _type_: _description_
        """
        async with Database().async_session() as session:
            yield session
