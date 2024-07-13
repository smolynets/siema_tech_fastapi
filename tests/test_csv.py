import io

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.items.crud import ProductCrud
from backend.items.models import Family, Product, Sale
from backend.main import app

product_crud = ProductCrud()


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