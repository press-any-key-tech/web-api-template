from sqlalchemy import text

from web_api_template.core.logging import logger
from web_api_template.core.repository.manager.sqlalchemy.async_database import (
    AsyncDatabase,
)
from web_api_template.domain.repository import HealthcheckRepository


class HealthcheckRepositoryImpl(HealthcheckRepository):
    """Repository implementation for Healtcheck"""

    async def verify(self) -> bool:
        """Verify database connection

        Raises:
            ie: _description_
            ex: _description_

        Returns:
            bool: _description_
        """

        try:
            logger.debug("Checking database health")
            # Run a simple query to check connection
            async with AsyncDatabase.get_session(self._label) as session:
                await session.execute(text("SELECT 1"))
                return True
        except Exception as ex:
            logger.exception("AsyncDatabase connection error")
            return False
