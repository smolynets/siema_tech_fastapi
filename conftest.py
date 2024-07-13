import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient  # Change to AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend import config
from backend.database import Base, SessionLocal, get_db
from backend.items.crud import ProductCrud
from backend.items.models import Family, Product, Sale
from backend.main import app

product_crud = ProductCrud()

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


@pytest.fixture
def create_families(db_session):
    def _create_families(count):
        assert db_session.query(Family).count() == 0
        for i in range(count):
            product_crud.create_family(db_session, f"Test Family {i+1}")
        assert db_session.query(Family).count() == count
    return _create_families


@pytest.fixture
def create_products(db_session):
    def _create_products(count, family_name):
        assert db_session.query(Product).count() == 0
        for i in range(count):
            product_crud.create_product(db_session, i+1, f"Test Product {i+1}", i+1, family_name)
        assert db_session.query(Product).count() == count
    return _create_products


@pytest.fixture
def create_sales(db_session):
    def _create_sales(count, product_id):
        assert db_session.query(Sale).count() == 0
        sales = {}
        for i in range(count):
            sales[f"2024-{i+1}"] = i+1
        product_crud.create_sales(db_session, sales, product_id)
        assert db_session.query(Sale).count() == count
    return _create_sales