from web_api_template.core.di_injector import inject
from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.domain.entities import Policy, PolicyFilter
from web_api_template.domain.entities.policy_create import PolicyCreate
from web_api_template.domain.exceptions import PolicyNotFoundException
from web_api_template.domain.repository import PolicyRepository


class WriteService:
    """Command operations"""

    @inject()
    def __init__(self, policy_db_repo: PolicyRepository):
        self.policy_db_repo = policy_db_repo

    async def create(
        self,
        # current_user: User,
        request: PolicyCreate,
    ) -> Policy:
        """
        Create a Policy.

        Args:
            current_user (User): The current user creating the policy.
            request (Policy): The requested policy to create.

        Returns:
            Policy: The newly created policy in the response format.
        """

        logger.debug("Entering. policy: %s", request)

        # if not await can_create(current_user=current_user):
        #     raise NotAllowedCreationException(
        #         "You are not allowed to create this item"
        #     )

        response: Policy = await self.policy_db_repo.create(
            # current_user=current_user,
            entity=request
        )

        return response

    async def delete_by_id(self, id: str):
        """
        Delete the Policy object with the given ID

        Args:
            id (UUID): ID of the policy to be deleted
            current_user (User): User object who is performing the deletion

        Raises:
            PolicyModificationNotAllowedException: If the current user is not allowed to modify the given policy
            PolicyNotFoundException: If the policy with the given ID is not found in the database

        Returns:
            None
        """

        logger.debug("Entering. id: %s", id)

        try:
            await self.policy_db_repo.delete(id=id)

        except ItemNotFoundException:
            # Domain exception raise if policy doesn't exists
            raise PolicyNotFoundException(f"Policy with id [{id}] not found")

    async def update(
        self,
        id: str,
        request: PolicyCreate,
        # current_user: User
    ) -> Policy:
        """
        Updates the given policy

        Args:
            id (UUID): Policy ID
            policy_request (Policy): New values for the Policy

        Returns:
            Policy: domain entity to return
        """

        logger.debug("Entering. id: %s request: %s", id, request)

        try:
            result: Policy = await self.policy_db_repo.update(id=id, policy=request)

            return result

        except ItemNotFoundException:
            # Domain exception raise if template does not exists
            raise PolicyNotFoundException(f"Policy with id [{id}] not found")
