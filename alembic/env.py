import os

# Import engine and application models
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))  # Add src to path
from web_api_template.core.repository.model.sqlalchemy import metadata

# Import Models (use # noqa: F401 for flake8 to ignore imports not used)
from web_api_template.infrastructure.models.sqlalchemy import AddressModel  # noqa: F401
from web_api_template.infrastructure.models.sqlalchemy import PersonModel  # noqa: F401
from web_api_template.infrastructure.models.sqlalchemy import PolicyModel  # noqa: F401
from web_api_template.infrastructure.models.sqlalchemy import (  # noqa: F401
    PermissionsModel,
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Get the database URL from the config
config = context.config
db_url = config.get_main_option("sqlalchemy.url")

# Create an engine
engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

# Get the dialect name
db_dialect = engine.dialect.name


# Store the dialect in the Alembic context
context.configure(
    connection=engine.connect(),
    target_metadata=target_metadata,
    compare_type=True,
    render_as_batch=True,
    dialect_name=db_dialect,
)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_name=db_dialect,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            dialect_name=db_dialect,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
