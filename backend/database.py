from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(
    settings.database_url
)

Sessionlocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False,
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
