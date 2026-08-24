from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from url_designer.infrastructure.database.config import get_database_url
from url_designer.infrastructure.database.models.url_record import UrlRecord


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importing the infrastructure model registers it with SQLModel.metadata before
# Alembic evaluates the schema for autogeneration.
target_metadata = SQLModel.metadata
config.set_main_option("sqlalchemy.url", get_database_url())


def run_migrations_offline() -> None:
    """Run migrations without connecting to the database."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with a database connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
