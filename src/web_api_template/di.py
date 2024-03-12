"""Dependency injection definition
"""

from pythondi import Provider

from web_api_template.core.logging import logger
from web_api_template.domain.repository import (
    AddressReadRepository,
    AddressWriteRepository,
    ContentReadRepository,
    ContentWriteRepository,
    HealthcheckRepository,
    PersonReadRepository,
    PersonWriteRepository,
    PolicyReadRepository,
    PolicyWriteRepository,
)
from web_api_template.infrastructure.repositories.sqlalchemy import (
    AddressReadRepositoryImpl,
    AddressWriteRepositoryImpl,
    ContentReadRepositoryImpl,
    ContentWriteRepositoryImpl,
    HealthcheckRepositoryImpl,
    PersonReadRepositoryImpl,
    PersonWriteRepositoryImpl,
    PolicyReadRepositoryImpl,
    PolicyWriteRepositoryImpl,
)


def include_di(provider: Provider):
    """Initialize dependency injection for repositories

    Args:
        provider (Provider): _description_
    """

    logger.debug("Initializing dependency injection")

    # Include your modules
    provider.bind(HealthcheckRepository, HealthcheckRepositoryImpl(), lazy=True)
    provider.bind(PersonReadRepository, PersonReadRepositoryImpl(), lazy=True)
    provider.bind(PolicyReadRepository, PolicyReadRepositoryImpl(), lazy=True)
    provider.bind(ContentReadRepository, ContentReadRepositoryImpl(), lazy=True)
    provider.bind(AddressReadRepository, AddressReadRepositoryImpl(), lazy=True)
    provider.bind(PersonWriteRepository, PersonWriteRepositoryImpl(), lazy=True)
    provider.bind(PolicyWriteRepository, PolicyWriteRepositoryImpl(), lazy=True)
    provider.bind(ContentWriteRepository, ContentWriteRepositoryImpl(), lazy=True)
    provider.bind(AddressWriteRepository, AddressWriteRepositoryImpl(), lazy=True)
