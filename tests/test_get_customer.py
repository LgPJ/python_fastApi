def test_get_customer_returns_customer(client):
    created = client.post("/customers", json={"name": "Ana", "email": "ana@example.com"}).json()

    response = client.get(f"/customers/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_customer_not_found_returns_404(client):
    response = client.get("/customers/999")

    assert response.status_code == 404
    assert "999" in response.json()["detail"]


def test_get_customer_invalid_id_returns_422(client):
    assert client.get("/customers/abc").status_code == 422
