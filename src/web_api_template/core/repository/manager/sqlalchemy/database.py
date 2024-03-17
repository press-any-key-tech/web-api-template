from contextlib import asynccontextmanager
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from web_api_template.core.logging import logger
from web_api_template.core.repository.model.sqlalchemy import metadata

from .settings import settings


class Database:
    _instance = None
    _engine = None
    _async_session = None

    _engines: Dict[str, AsyncEngine] = {}
    _sessions: Dict[str, AsyncSession] = {}

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

    def init_engines(self):
        """Initialize all engines"""

        if not self._engines:
            self._engines = {}
            self._sessions = {}
            for label in settings.labels:
                self._engines[label] = create_async_engine(
                    settings.get_settings(label).DATABASE_URI,
                    pool_pre_ping=settings.get_settings(label).POOL_PRE_PING,
                    pool_size=settings.get_settings(label).POOL_SIZE,
                    echo=settings.get_settings(label).ECHO_POOL,
                    max_overflow=settings.get_settings(label).MAX_OVERFLOW,
                    pool_recycle=settings.get_settings(label).POOL_RECYCLE_IN_SECONDS,
                    echo_pool=settings.get_settings(label).ECHO_POOL,
                    pool_reset_on_return=settings.get_settings(
                        label
                    ).POOL_RESET_ON_RETURN,
                    pool_timeout=settings.get_settings(label).POOL_TIMEOUT_IN_SECONDS,
                )
                self._sessions[label] = sessionmaker(
                    self._engines[label], class_=AsyncSession, expire_on_commit=False
                )

    def async_session(self, label: str = "DEFAULT"):
        if not self._sessions:
            self.init_engines()
        return self._sessions[label]

    @property
    def engine(self, label: str = "DEFAULT"):
        if not self._engines:
            self.init_engines()
        return self._engines[label]

    def get_engine(self, label: str = "DEFAULT"):
        """Get engine by label

        Args:
            label (str, optional): _description_. Defaults to "DEFAULT".

        Returns:
            _type_: _description_
        """
        if not self._engines:
            self.init_engines()
        return self._engines[label]

    @staticmethod
    @asynccontextmanager
    async def get_db_session(label: str = "DEFAULT"):
        """Gets a session from database

        Yields:
            _type_: _description_
        """
        # Async session returns a sessión factory (sessionmaker) and it needs () to create a session
        async with Database().async_session(label)() as session:
            yield session

    @staticmethod
    async def initialize(label: str = None):
        """Initialize database (if active in settings)

        Args:
            label (str, optional): _description_. Defaults to None.
        """
        labels = [label] if label else settings.labels
        for label in labels:
            if settings.get_settings(label).INITIALIZE:
                async with Database().get_engine(label).begin() as conn:
                    logger.debug("Creating tables for: %s", label)
                    await conn.run_sync(metadata.create_all)
