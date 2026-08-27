import pytest
from app.core.database import Base, engine, SessionLocal
from app.seed.seed_data import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    yield
