import pytest
import requests

BASE = "http://localhost:8000"


@pytest.mark.skipif(True, reason="Run in CI/integration environment with backend up")
def test_order_idempotency():
    """Posts the same order twice with the same Idempotency-Key and asserts only one order is created and same response returned."""
    url = f"{BASE}/api/v1/orders"
    payload = {"items": [{"productId": "prod-1", "quantity": 1, "price": 9.99}]}
    headers = {"Idempotency-Key": "test-key-123"}

    r1 = requests.post(url, json=payload, headers=headers)
    assert r1.status_code in (200, 201)
    data1 = r1.json()

    r2 = requests.post(url, json=payload, headers=headers)
    assert r2.status_code == r1.status_code
    data2 = r2.json()

    assert data1.get("id") == data2.get("id")


@pytest.mark.skipif(True, reason="Run in CI/integration environment with backend up")
def test_idempotency_conflict():
    """Posts two requests with same Idempotency-Key but different payloads and expects 409."""
    url = f"{BASE}/api/v1/orders"
    payload1 = {"items": [{"productId": "prod-1", "quantity": 1, "price": 9.99}]}
    payload2 = {"items": [{"productId": "prod-2", "quantity": 2, "price": 5.00}]}
    headers = {"Idempotency-Key": "test-key-conflict"}

    r1 = requests.post(url, json=payload1, headers=headers)
    assert r1.status_code in (200, 201)

    r2 = requests.post(url, json=payload2, headers=headers)
    assert r2.status_code == 409
