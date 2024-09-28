from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

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
SQLModel.metadata.create_all(engine)


def get_database_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
