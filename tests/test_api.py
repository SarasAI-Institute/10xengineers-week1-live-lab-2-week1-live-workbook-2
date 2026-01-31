import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.storage import products, categories, stock, movements

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear():
    products.clear()
    categories.clear()
    stock.clear()
    movements.clear()

def test_create_product():
    r = client.post("/products", json={
        "name": "Widget",
        "sku": "WD-1234-001",
        "price": 9.99
    })
    assert r.status_code == 200

def test_list_empty():
    r = client.get("/products")
    assert r.json() == []

def test_adjust_stock():
    p = client.post("/products", json={
        "name": "Test",
        "sku": "TS-0000-001",
        "price": 5.00
    }).json()
    r = client.post(f"/stock/{p['id']}/adjust", json={
        "quantity": 50,
        "reason": "initial stock"
    })
    assert r.status_code == 200
    assert r.json()["new"] == 50

