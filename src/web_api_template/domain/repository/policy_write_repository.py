from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.entities import Policy, PolicyFilter


class PolicyWriteRepository(RepositoryBase):
    """
    Abstract class for database policy repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def create(self, *, entity: Policy) -> Optional[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, policy: Policy) -> Optional[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()