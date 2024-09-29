from abc import abstractmethod
from typing import Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.aggregates import Policy, PolicyCreate


class PolicyWriteRepository(RepositoryBase):
    """
    Abstract class for database policy repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def create(
        self, *, person_id: str, entity: PolicyCreate
    ) -> Optional[PolicyCreate]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, policy: Policy) -> Optional[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
