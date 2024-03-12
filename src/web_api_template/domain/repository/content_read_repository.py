from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.domain.entities import Content, ContentFilter


class ContentReadRepository(metaclass=ABCMeta):
    """
    Abstract class for database content repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Content]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, *, filter: ContentFilter) -> List[Content]:
        raise NotImplementedError()

    @abstractmethod
    async def get_list_by_policy_id(self, *, id: str) -> List[Content]:
        raise NotImplementedError()
