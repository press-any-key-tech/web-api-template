"""Dependency injection definition
"""

from pydilite import Provider

from web_api_template.core.logging import logger
from web_api_template.domain.repository import (
    AddressReadRepository,
    AddressWriteRepository,
    HealthcheckRepository,
    PermissionsReadRepository,
    PersonReadRepository,
    PersonWriteRepository,
    PolicyReadRepository,
    PolicyWriteRepository,
)

# from web_api_template.infrastructure.repositories.dynamodb import (
#     PersonReadRepositoryImpl,
#     PersonWriteRepositoryImpl,
# )
from web_api_template.infrastructure.repositories.sqlalchemy import (
    AddressReadRepositoryImpl,
    AddressWriteRepositoryImpl,
    HealthcheckRepositoryImpl,
    PermissionsReadRepositoryImpl,
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

    # ----------------------------------------
    # Include your modules
    # ----------------------------------------

    provider.bind(
        HealthcheckRepository,
        HealthcheckRepositoryImpl(label="DEFAULT"),  # type: ignore
        lazy=True,
    )
    provider.bind(
        PersonReadRepository,
        PersonReadRepositoryImpl(label="DEFAULT"),  # type: ignore
        lazy=True,
    )
    provider.bind(
        PolicyReadRepository,
        PolicyReadRepositoryImpl(label="DEFAULT"),  # type: ignore
        lazy=True,
    )
    provider.bind(
        AddressReadRepository,
        AddressReadRepositoryImpl(label="DEFAULT"),  # type: ignore
        lazy=True,
    )
    provider.bind(
        PersonWriteRepository,
        PersonWriteRepositoryImpl(label="DEFAULT"),  # type: ignore
        lazy=True,
    )
    provider.bind(
        PolicyWriteRepository,
        PolicyWriteRepositoryImpl(label="DEFAULT"),  # type: ignore
        lazy=True,
    )
    provider.bind(
        AddressWriteRepository,
        AddressWriteRepositoryImpl(label="DEFAULT"),  # type: ignore
        lazy=True,
    )
    provider.bind(
        PermissionsReadRepository,
        PermissionsReadRepositoryImpl(label="DEFAULT"),  # type: ignore
        lazy=True,
    )

    logger.debug("Dependency injection initialization completed ...")
