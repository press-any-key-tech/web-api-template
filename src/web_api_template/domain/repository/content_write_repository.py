from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.entities import Content, ContentCreate, ContentFilter


class ContentWriteRepository(RepositoryBase):
    """
    Abstract class for database content repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def create(self, *, entity: ContentCreate) -> Optional[Content]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, content: Content) -> Optional[Content]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
