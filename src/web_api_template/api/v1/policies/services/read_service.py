from typing import List

from web_api_template.core.di_injector import inject
from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities import Policy, PolicyFilter
from web_api_template.domain.exceptions import PolicyNotFoundException
from web_api_template.domain.repository import PolicyRepository


class ReadService:
    """Query operations"""

    @inject()
    def __init__(self, policy_db_repo: PolicyRepository):
        self.policy_db_repo = policy_db_repo

    async def get_list(self, filter: PolicyFilter) -> List[Policy]:
        """
        Get a list of policys

        Args:
            filter (PolicyFilter): Policy related filter

        Returns:
            List[Policy]: domain entity to return
        """

        logger.debug("Entering. filter: %s", filter)

        entities: List[Policy] = await self.policy_db_repo.get_list(filter=filter)

        return entities

    async def get_by_id(self, id: str) -> Policy:
        """
        Search policy by id

        Args:
            id (str): id of the policy

        Returns:
            policy: domain entity to return
        """

        logger.debug("Entering. id: %s", id)

        try:
            entity: Policy | None = await self.policy_db_repo.get_by_id(id=id)
        except ItemNotFoundException:
            # Domain exception raise if pot doesn't exists
            raise PolicyNotFoundException(f"Policy with id [{id}] not found")

        return entity

    async def get_list_by_person_id(self, id: str) -> List[Policy]:
        """
        Get a list of policys for a given person

        Args:
            id (str): Person id

        Returns:
            List[Policy]: domain entity to return
        """

        logger.debug("Entering. filter: %s", id)

        entities: List[Policy] = await self.policy_db_repo.get_list_by_person_id(id=id)

        return entities
