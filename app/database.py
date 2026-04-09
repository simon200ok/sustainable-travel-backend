from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

#Old
# def _engine_kwargs() -> dict:
#     # SQLite requires check_same_thread=False for use with FastAPI's threaded workers
#     if "sqlite" in settings.database_url:
#         return {"connect_args": {"check_same_thread": False}}
#     return {}

#New
def _engine_kwargs() -> dict:
    database_url = settings.resolved_database_url

    if database_url.startswith("sqlite"):
        return {
            "connect_args": {"check_same_thread": False},
        }

    return {
        "pool_pre_ping": True,
    }

#Old
# engine = create_engine(settings.database_url, **_engine_kwargs())

#New
engine = create_engine(settings.resolved_database_url, **_engine_kwargs())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
