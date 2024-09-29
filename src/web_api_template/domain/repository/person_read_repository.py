from abc import ABCMeta, abstractmethod
from typing import List, Optional

from web_api_template.core.api.pagination_query_model import PaginationQueryModel
from web_api_template.core.repository.manager.sqlalchemy.page import Page
from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)
from web_api_template.domain.entities.person import Person
from web_api_template.domain.entities.person_create import PersonCreate
from web_api_template.domain.entities.person_filter import PersonFilter


class PersonReadRepository(RepositoryBase):
    """
    Abstract class for database person repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Person]:
        raise NotImplementedError()

    @abstractmethod
    async def get_paginated_list(
        self, *, filter: PersonFilter, pagination: PaginationQueryModel
    ) -> Page:
        raise NotImplementedError()

    # @abstractmethod
    # async def get_list(self, *, filter: PersonsFilter, query: CommonQueryModel) -> dict:
    #     raise NotImplementedError()
