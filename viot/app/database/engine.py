import logging
import sys

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .config import db_settings

logger = logging.getLogger(__name__)


def create_engine() -> AsyncEngine:
    try:
        async_engine = create_async_engine(
            db_settings.SQLALCHEMY_DATABASE_URI,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=20,
            pool_recycle=60 * 60,  # 60 minutes
            pool_use_lifo=True,
        )
    except Exception as e:
        logger.error(f"Error while creating async engine: {e}")
        sys.exit(1)
    return async_engine


async_engine = create_engine()
