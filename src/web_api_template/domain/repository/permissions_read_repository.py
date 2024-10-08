from abc import abstractmethod
from typing import List, Optional

from web_api_template.core.repository.manager.sqlalchemy.repository_base import (
    RepositoryBase,
)


class PermissionsReadRepository(RepositoryBase):
    """
    Abstract class for database permissions repository

    Raises:
        NotImplementedError: _description_
    """

    @abstractmethod
    async def get_permissions_by_username(self, *, username: str) -> List[str]:
        raise NotImplementedError()
