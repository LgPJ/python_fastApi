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
