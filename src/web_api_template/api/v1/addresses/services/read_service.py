from typing import List, Optional

from pydilite import inject

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.exceptions import AddressNotFoundException
from web_api_template.domain.repository import AddressReadRepository
from web_api_template.domain.value_objects.address import Address
from web_api_template.domain.value_objects.address_filter import AddressFilter


class ReadService:
    """Query operations"""

    @inject()
    def __init__(self, address_db_repo: AddressReadRepository):
        self.address_db_repo = address_db_repo

    async def get_list_by_person_id(self, person_id: str) -> List[Address]:
        """
        Get a list of addresses

        Args:
            person_id (str): person id
            filter (AddressFilter): Address related filter

        Returns:
            List[Address]: domain entity to return
        """

        logger.debug(f"Entering. person: {person_id}")

        entities: List[Address] = await self.address_db_repo.get_list_by_person_id(
            person_id=person_id
        )

        return entities

    async def get_list(self, filter: AddressFilter) -> List[Address]:
        """
        Get a list of addresses

        Args:
            filter (AddressFilter): Address related filter

        Returns:
            List[Address]: domain entity to return
        """

        logger.debug("Entering. filter: {}", filter)

        entities: List[Address] = await self.address_db_repo.get_list(filter=filter)

        return entities

    async def get_by_id(self, id: str) -> Optional[Address]:
        """
        Search address by id

        Args:
            id (str): id of the address

        Returns:
            address: domain entity to return
        """

        logger.debug("Entering. id: {}", id)

        try:
            entity: Optional[Address] = await self.address_db_repo.get_by_id(id=id)
        except ItemNotFoundException:
            # Domain exception raise if pot doesn't exists
            raise AddressNotFoundException(id=id)

        return entity
