import time
import requests
import pytest

BASE = "http://localhost:8000"


@pytest.mark.skipif(True, reason="Run in CI where backend is running")
def test_products_list_response_time():
    url = f"{BASE}/api/v1/products"
    start = time.time()
    r = requests.get(url, timeout=5)
    elapsed = time.time() - start
    assert r.status_code == 200
    assert elapsed < 2.0, f"Response too slow: {elapsed}s"
