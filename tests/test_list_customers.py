import pytest


def _create(client, name, email):
    return client.post("/customers", json={"name": name, "email": email}).json()


def test_list_customers_returns_all(client):
    _create(client, "Ana", "ana@example.com")
    _create(client, "Beto", "beto@example.com")

    response = client.get("/customers")

    assert response.status_code == 200
    assert [c["email"] for c in response.json()] == ["ana@example.com", "beto@example.com"]


def test_list_customers_empty(client):
    assert client.get("/customers").json() == []


def test_list_customers_filters_by_status(client):
    _create(client, "Ana", "ana@example.com")

    assert len(client.get("/customers", params={"status": "PENDING"}).json()) == 1
    assert client.get("/customers", params={"status": "ACTIVE"}).json() == []


def test_list_customers_rejects_invalid_status(client):
    response = client.get("/customers", params={"status": "NOPE"})

    assert response.status_code == 422


def test_list_customers_paginates_with_total_header(client):
    for i in range(5):
        _create(client, f"C{i}", f"c{i}@example.com")

    response = client.get("/customers", params={"limit": 2, "offset": 2})

    assert response.status_code == 200
    assert [c["email"] for c in response.json()] == ["c2@example.com", "c3@example.com"]
    assert response.headers["X-Total-Count"] == "5"


def test_list_customers_offset_past_end_returns_empty(client):
    _create(client, "Ana", "ana@example.com")

    response = client.get("/customers", params={"offset": 10})

    assert response.json() == []
    assert response.headers["X-Total-Count"] == "1"


def test_list_customers_total_respects_status_filter(client):
    _create(client, "Ana", "ana@example.com")
    _create(client, "Beto", "beto@example.com")
    client.patch("/customers/1/status", json={"status": "ACTIVE"})

    response = client.get("/customers", params={"status": "ACTIVE", "limit": 1})

    assert len(response.json()) == 1
    assert response.headers["X-Total-Count"] == "1"




@pytest.mark.parametrize("params", [{"limit": 0}, {"limit": 101}, {"offset": -1}, {"limit": "x"}])
def test_list_customers_rejects_invalid_pagination(client, params):
    assert client.get("/customers", params=params).status_code == 422
