"""
    Startup and shutdown code for the whole application
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from web_api_template.core.logging import logger
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.infrastructure.models.dynamodb import (
    ContentModel,
    PersonModel,
    PolicyModel,
)


async def initialize_dynamodb():
    """Initialize the Dynamodb database"""

    logger.debug("Initializing DYNAMODB database ...")

    # Initialize each model
    if not PersonModel.exists():
        # TODO: add read/write capacity units to settings
        PersonModel.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
            wait=True,
        )
        logger.debug("* PersonModel created")

    if not PolicyModel.exists():
        # TODO: add read/write capacity units to settings
        PolicyModel.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
            wait=True,
        )
        logger.debug("* PolicyModel created")

    if not ContentModel.exists():
        # TODO: add read/write capacity units to settings
        ContentModel.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
            wait=True,
        )
        logger.debug("* ContentModel created")

    logger.debug("DYNAMODB database initialized ...")


async def initialize_sqlalchemy():
    """
    Initialize SQLALCHEMY database
    """
    logger.debug("Initializing SQLALCHEMY database ...")
    await Database.initialize()
    logger.debug("SQLALCHEMY database initialized")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous initilizations on startup/shutdown
    Substitute old app.on_event("startup")
    """

    # --------------------------------------------------------------
    # Startup section
    # --------------------------------------------------------------

    # Initialize SQLALCHEMY database
    await initialize_sqlalchemy()

    # Initialize DynamoDB database
    await initialize_dynamodb()

    logger.info("Async startup completed ...")

    yield

    # --------------------------------------------------------------
    # Shutdown section
    # --------------------------------------------------------------

    logger.info("Async shutdown completed ...")
