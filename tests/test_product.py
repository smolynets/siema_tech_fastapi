from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient


from backend.main import app
from backend.items.models import Product, Family
from backend.items.crud import ProductCrud




product_crud = ProductCrud()


def test_get_all_products(test_client, db_session):
    # Create test data
    test_product = Family(name="Test Product")
    db_session.add(test_product)
    db_session.commit()
    db_session.refresh(test_product)

    # Test the endpoint
    response = test_client.get("/api/v1/items/families/?skip=0&limit=10")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == "Test Product"