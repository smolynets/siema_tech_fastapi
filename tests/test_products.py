import io
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient


from backend.main import app
from backend.items.models import Product, Family, Sale
from backend.items.crud import ProductCrud


product_crud = ProductCrud()


def test_get_no_products(test_client, db_session):
    assert db_session.query(Product).count() == 0
    response = test_client.get("/api/v1/items/products/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize("num_products", [1, 3, 5, 10])
def test_get_products(test_client, db_session, create_families, create_products, num_products):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    create_products(num_products, created_family.name)
    response = test_client.get("/api/v1/items/products/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == num_products
    assert response.json()[0]['name']


def test_get_product_by_id(test_client, db_session, create_families, create_products):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    create_products(1, created_family.name)
    created_product = db_session.query(Product).order_by(Product.id.desc()).first()
    response = test_client.get(f"/api/v1/items/product/{created_product.id}")
    assert response.status_code == 200


def test_error_get_product_by_id(test_client, db_session):
    assert db_session.query(Product).count() == 0
    response = test_client.get("/api/v1/items/product/1")
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Product not found"

def test_update_product(test_client, db_session, create_families, create_products):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    create_products(1, created_family.name)
    created_product = db_session.query(Product).order_by(Product.id.desc()).first()
    assert created_product.name == "Test Product 1"
    update_data = {
        "id": 22222,
        "name": "second name",
        "price": 2000
    }
    response = test_client.put(f"/api/v1/items/product/{created_product.id}", json=update_data)
    assert response.status_code == 200
    updated_product = db_session.query(Product).order_by(Product.id.desc()).first()
    assert updated_product.name == "second name"


def test_delete_product(test_client, db_session, create_families, create_products):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    create_products(1, created_family.name)
    created_product = db_session.query(Product).order_by(Product.id.desc()).first()
    response = test_client.delete(f"/api/v1/items/delete_product/{created_product.id}")
    assert response.status_code == 200
    assert db_session.query(Product).count() == 0


def test_error_delete_product(test_client, db_session):
    assert db_session.query(Product).count() == 0
    response = test_client.delete("/api/v1/items/delete_product/1")
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Product not found"