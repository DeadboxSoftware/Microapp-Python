import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Import your models and Base
from database import Base
from models import User

# Alembic Config object, provides access to values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support.
target_metadata = Base.metadata

# Function to run migrations asynchronously
def run_migrations_online():
    """Run migrations in 'online' mode using async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_migrations)

    def do_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Ensure column types are compared
            compare_server_default=True,  # Compare server default values
        )

        with context.begin_transaction():
            context.run_migrations()

    # Run the async migration in an asyncio event loop
    asyncio.run(do_run_migrations())

run_migrations_online()
