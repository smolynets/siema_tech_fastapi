import pytest
from httpx import AsyncClient  # Change to AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import Base, get_db, SessionLocal
from backend import config
from fastapi.testclient import TestClient
from backend import config

# Update the URL to match your Docker Compose setup
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{config.TEST_POSTGRES_USER}:{config.TEST_POSTGRES_PASSWORD}@{config.TEST_POSTGRES_HOST}:\
    {config.TEST_POSTGRES_PORT}/{config.TEST_DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    with engine.begin() as conn:
        Base.metadata.create_all(conn)  # Create the schema
    yield
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)  # Drop the schema

def override_get_db():
    def _override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    return _override_get_db

# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db()

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client