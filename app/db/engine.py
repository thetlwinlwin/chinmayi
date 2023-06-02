from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.settings import app_settings

SQLALCHEMY_DATABASE_URL_OBJ = URL.create(
    drivername=" postgresql+psycopg2",
    database="postgresql",
    username=app_settings.db_username,
    host=app_settings.db_hostname,
    password=app_settings.db_password,
    port=app_settings.db_port,
)

SQLALCHEMY_DATABASE_URL = f"postgresql://{app_settings.db_username}:{app_settings.db_password}@{app_settings.db_hostname}:{app_settings.db_port}/{app_settings.db_name}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
