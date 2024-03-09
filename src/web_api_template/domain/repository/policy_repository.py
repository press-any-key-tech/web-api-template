from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.domain.entities import Policy, PolicyFilter


class PolicyRepository(metaclass=ABCMeta):
    """
    Abstract class for database policy repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, *, filter: PolicyFilter) -> List[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list_by_person_id(self, *, id: str) -> List[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def create(self, *, entity: Policy) -> Optional[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *, id: str, policy: Policy) -> Optional[Policy]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *, id: str):
        return NotImplementedError()
