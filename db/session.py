from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.base import DATABASE_URL, DEBUG

engine = create_engine(DATABASE_URL, echo=DEBUG)
db_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def get_session():
    with db_session() as session:
        try:
            yield session
        finally:
            session.close()
