"""Dependency injection definition
"""

from pythondi import Provider

from web_api_template.core.logging import logger
from web_api_template.domain.repository import (
    HealthcheckRepository,
    PersonRepository,
    PolicyRepository,
)
from web_api_template.infrastructure.repositories.postgresql.healthcheck_repository_impl import (
    HealthcheckRepositoryImpl,
)
from web_api_template.infrastructure.repositories.postgresql.person_repository_impl import (
    PersonRepositoryImpl,
)
from web_api_template.infrastructure.repositories.postgresql.policy_repository_impl import (
    PolicyRepositoryImpl,
)


def include_di(provider: Provider):
    """Initialize dependency injection for repositories

    Args:
        provider (Provider): _description_
    """

    logger.debug("Initializing dependency injection")

    # Include your modules
    provider.bind(HealthcheckRepository, HealthcheckRepositoryImpl)
    provider.bind(PersonRepository, PersonRepositoryImpl)
    provider.bind(PolicyRepository, PolicyRepositoryImpl)
