def test_create_customer_returns_201_with_pending_status(client):
    response = client.post("/customers", json={"name": "Juan Pérez", "email": "juan@example.com"})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == "Juan Pérez"
    assert body["email"] == "juan@example.com"
    assert body["status"] == "PENDING"
    assert body["created_at"]


def test_create_customer_rejects_duplicate_email(client):
    payload = {"name": "Juan", "email": "juan@example.com"}
    client.post("/customers", json=payload)

    response = client.post("/customers", json={"name": "Otro", "email": "JUAN@example.com"})

    assert response.status_code == 409


def test_create_customer_rejects_invalid_email(client):
    response = client.post("/customers", json={"name": "Juan", "email": "not-an-email"})

    assert response.status_code == 422


def test_create_customer_rejects_blank_name(client):
    response = client.post("/customers", json={"name": "   ", "email": "a@example.com"})

    assert response.status_code == 422
