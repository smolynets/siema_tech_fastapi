import io
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient


from backend.main import app
from backend.items.models import Product, Family, Sale
from backend.items.crud import ProductCrud


product_crud = ProductCrud()


# families

def test_get_no_families(test_client, db_session):
    assert db_session.query(Family).count() == 0
    response = test_client.get("/api/v1/items/families/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.parametrize("num_families", [1, 3, 5, 10])
def test_get_families(test_client, db_session, create_families, num_families):
    create_families(num_families)
    response = test_client.get("/api/v1/items/families/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) == num_families
    assert response.json()[0]['name']


def test_get_family_by_id(test_client, db_session, create_families):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    response = test_client.get(f"/api/v1/items/family/{created_family.id}")
    assert response.status_code == 200
    assert response.json() == {'name': 'Test Family 1', 'id': created_family.id}


def test_error_get_family_by_id(test_client, db_session):
    assert db_session.query(Family).count() == 0
    response = test_client.get("/api/v1/items/family/1")
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Family not found"

def test_update_family(test_client, db_session, create_families):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    assert created_family.name == "Test Family 1"
    update_data = {
        "name": "second name"
    }
    response = test_client.put(f"/api/v1/items/family/{created_family.id}", json=update_data)
    assert response.status_code == 200
    updated_family = db_session.query(Family).order_by(Family.id.desc()).first()
    assert updated_family.name == "second name"


def test_delete_family(test_client, db_session, create_families):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    response = test_client.delete(f"/api/v1/items/delete_family/{created_family.id}")
    assert response.status_code == 200
    assert db_session.query(Family).count() == 0


def test_error_delete_family(test_client, db_session):
    assert db_session.query(Family).count() == 0
    response = test_client.delete("/api/v1/items/delete_family/1")
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Family not found"


# products

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


# sales

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


def test_upload_csv(test_client, db_session):
    with open('test_data.csv', 'rb') as f:
        file = io.BytesIO(f.read())
    files = {'file': ('test_data.csv', file, 'text/csv')}
    response = test_client.post("/api/v1/items/upload-csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Products uploaded successfully"}
    products = db_session.query(Product).all()
    assert len(products) == 5
    
    sales = db_session.query(Sale).all()
    assert len(sales) == 20

    families = db_session.query(Family).all()
    assert len(families) == 3

    product = db_session.query(Product).filter_by(id=1111).first()
    assert product.name == "Blue Candy"
    assert product.price == 10.0
    assert product.family.name == "Candy"
    sale = db_session.query(Sale).filter_by(product_id=1111).first()
    assert sale.month == "2024-01"
    assert sale.count == 23


@pytest.mark.parametrize("filename,content_type,expected_status_code", [
    ("test.txt", "text/plain", 400),
    ("test.csv", "application/octet-stream", 400)
])
def test_upload_invalid_files(test_client, filename, content_type, expected_status_code):
    file = io.BytesIO(b"Product ID,Product Name,Family,Price,January,February,March\n1,Test Product,Test Family,10.0,5,3,8")
    file.name = filename
    files = {'file': (filename, file, content_type)}
    response = test_client.post("/api/v1/items/upload-csv/", files=files)
    assert response.status_code == expected_status_code
    assert response.json()["detail"][0]["msg"] == "Invalid file type. Only CSV files are allowed."