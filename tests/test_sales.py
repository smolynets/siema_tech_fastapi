import io
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient


from backend.main import app
from backend.items.models import Product, Family, Sale
from backend.items.crud import ProductCrud


product_crud = ProductCrud()


def test_get_no_sales(test_client, db_session):
    assert db_session.query(Sale).count() == 0
    response = test_client.get("/api/v1/items/sales/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize("num_sales", [1, 3, 5, 10])
def test_get_sales(test_client, db_session, create_families, create_products, create_sales, num_sales):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    create_products(1, created_family.name)
    created_product = db_session.query(Product).order_by(Product.id.desc()).first()
    create_sales(num_sales, created_product.id)
    response = test_client.get("/api/v1/items/sales/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == num_sales
    assert response.json()[0]['count']


def test_get_sale_by_id(test_client, db_session, create_families, create_products, create_sales):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    create_products(1, created_family.name)
    created_product = db_session.query(Product).order_by(Product.id.desc()).first()
    create_sales(1, created_product.id)
    created_sale = db_session.query(Sale).order_by(Sale.id.desc()).first()
    response = test_client.get(f"/api/v1/items/sale/{created_sale.id}")
    assert response.status_code == 200


def test_error_get_sale_by_id(test_client, db_session):
    assert db_session.query(Product).count() == 0
    response = test_client.get("/api/v1/items/sale/1")
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Sale not found"

def test_update_sale(test_client, db_session, create_families, create_products, create_sales):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    create_products(1, created_family.name)
    created_product = db_session.query(Product).order_by(Product.id.desc()).first()
    create_sales(1, created_product.id)
    created_sale = db_session.query(Sale).order_by(Sale.id.desc()).first()
    assert created_sale.month == "2024-1"
    update_data = {
        "month": "2024-2",
        "count": 2000
    }
    response = test_client.put(f"/api/v1/items/sale/{created_sale.id}", json=update_data)
    assert response.status_code == 200
    updated_product = db_session.query(Sale).order_by(Sale.id.desc()).first()
    assert created_sale.month == "2024-2"
    assert created_sale.count == 2000


def test_delete_sale(test_client, db_session, create_families, create_products, create_sales):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    create_products(1, created_family.name)
    created_product = db_session.query(Product).order_by(Product.id.desc()).first()
    create_sales(1, created_product.id)
    created_sale = db_session.query(Sale).order_by(Sale.id.desc()).first()
    response = test_client.delete(f"/api/v1/items/delete_sale/{created_sale.id}")
    assert response.status_code == 200
    assert db_session.query(Sale).count() == 0


def test_error_delete_sale(test_client, db_session):
    assert db_session.query(Sale).count() == 0
    response = test_client.delete("/api/v1/items/delete_sale/1")
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Sale not found"
