import pytest


def _create(client):
    return client.post("/customers", json={"name": "Ana", "email": "ana@example.com"}).json()


@pytest.mark.parametrize("new_status", ["ACTIVE", "BLOCKED", "PENDING"])
def test_update_status_changes_status(client, new_status):
    customer = _create(client)

    response = client.patch(f"/customers/{customer['id']}/status", json={"status": new_status})

    assert response.status_code == 200
    assert response.json()["status"] == new_status
    assert client.get(f"/customers/{customer['id']}").json()["status"] == new_status


def test_update_status_invalid_value_returns_422(client):
    customer = _create(client)

    response = client.patch(f"/customers/{customer['id']}/status", json={"status": "DELETED"})

    assert response.status_code == 422


def test_update_status_unknown_customer_returns_404(client):
    response = client.patch("/customers/999/status", json={"status": "ACTIVE"})

    assert response.status_code == 404
