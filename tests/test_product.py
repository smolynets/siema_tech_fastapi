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


def test_error_get_family_by_id(test_client, db_session):
    assert db_session.query(Family).count() == 0
    response = test_client.get("/api/v1/items/family/1")
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "Family not found"

def test_update_family(test_client, db_session, create_families):
    create_families(1)
    created_family = db_session.query(Family).order_by(Family.id.desc()).first()
    assert created_family.name == "Test Product 1"
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


