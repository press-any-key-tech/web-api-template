from web_api_template.core.di_injector import inject
from web_api_template.core.settings import settings
from web_api_template.domain.repository import HealthcheckRepository


class HealthcheckService:
    """Command operations"""

    @inject()
    def __init__(self, hc_db_repo: HealthcheckRepository):
        self.hc_db_repo = hc_db_repo

    async def verify(
        self,
    ) -> bool:
        """Verify the availability of the API services

        Returns:
            bool: _description_
        """

        # TODO: Verify every component, if needed
        return await self.hc_db_repo.verify() if settings.HEALTHCHECK_DATABASE else True
