from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from hackyeah_2024_ad_deviniti.config.config_models import get_db_config

SQLALCHEMY_DATABASE_URL = get_db_config().postgres_connection_string

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=4,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
)


def get_database_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
