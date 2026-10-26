def create_supplier_payload(**overrides):
    payload = {
        "supplier_name": "Test Supplier",
        "email": "supplier@example.com",
        "phone_number": "9876543210",
        "phone": "9876543210",
        "address": "Test Address",
        "company_name": "Test Company",
        "is_active": True,
    }
    payload.update(overrides)
    return payload


def test_create_supplier(client):
    response = client.post(
        "/suppliers",
        json=create_supplier_payload(),
    )

    assert response.status_code == 201
    assert response.json()["supplier_name"] == "Test Supplier"
    assert response.json()["email"] == "supplier@example.com"


def test_list_suppliers(client):
    client.post(
        "/suppliers",
        json=create_supplier_payload(),
    )

    response = client.get("/suppliers")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["supplier_name"] == "Test Supplier"


def test_list_active_suppliers(client):
    client.post(
        "/suppliers",
        json=create_supplier_payload(),
    )
    client.post(
        "/suppliers",
        json=create_supplier_payload(
            supplier_name="Inactive Supplier",
            email="inactive@example.com",
            is_active=False,
        ),
    )

    response = client.get("/suppliers/active")

    assert response.status_code == 200
    assert all(supplier["is_active"] for supplier in response.json())


def test_get_supplier(client):
    create_response = client.post(
        "/suppliers",
        json=create_supplier_payload(),
    )
    supplier_id = create_response.json()["supplier_id"]

    response = client.get(f"/suppliers/{supplier_id}")

    assert response.status_code == 200
    assert response.json()["supplier_id"] == supplier_id


def test_update_supplier(client):
    create_response = client.post(
        "/suppliers",
        json=create_supplier_payload(),
    )
    supplier_id = create_response.json()["supplier_id"]

    response = client.put(
        f"/suppliers/{supplier_id}",
        json={
            "supplier_name": "Updated Supplier",
            "is_active": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["supplier_name"] == "Updated Supplier"
    assert response.json()["is_active"] is False


def test_delete_supplier(client):
    create_response = client.post(
        "/suppliers",
        json=create_supplier_payload(),
    )
    supplier_id = create_response.json()["supplier_id"]

    response = client.delete(f"/suppliers/{supplier_id}")

    assert response.status_code == 204

    get_response = client.get(f"/suppliers/{supplier_id}")
    assert get_response.status_code == 404


def test_missing_supplier_returns_not_found(client):
    response = client.get("/suppliers/99999")

    assert response.status_code == 404


def test_invalid_supplier_returns_validation_error(client):
    response = client.post(
        "/suppliers",
        json=create_supplier_payload(
            email="invalid-email",
        ),
    )

    assert response.status_code == 422
