def test_create_category(client):
    response = client.post(
        "/categories",
        json={
            "category_name": "Electronics",
            "description": "Electronic products",
        },
    )

    assert response.status_code == 201
    assert response.json()["category_name"] == "Electronics"
    assert response.json()["description"] == "Electronic products"
    assert "category_id" in response.json()


def test_list_categories(client):
    client.post(
        "/categories",
        json={
            "category_name": "Books",
            "description": "Printed books",
        },
    )

    response = client.get("/categories")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category_name"] == "Books"


def test_get_category(client):
    create_response = client.post(
        "/categories",
        json={
            "category_name": "Furniture",
            "description": "Home furniture",
        },
    )

    category_id = create_response.json()["category_id"]

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 200
    assert response.json()["category_name"] == "Furniture"


def test_update_category(client):
    create_response = client.post(
        "/categories",
        json={
            "category_name": "Clothing",
            "description": "Old description",
        },
    )

    category_id = create_response.json()["category_id"]

    response = client.put(
        f"/categories/{category_id}",
        json={
            "category_name": "Apparel",
            "description": "Updated description",
        },
    )

    assert response.status_code == 200
    assert response.json()["category_name"] == "Apparel"
    assert response.json()["description"] == "Updated description"


def test_delete_category(client):
    create_response = client.post(
        "/categories",
        json={
            "category_name": "Toys",
            "description": "Children's toys",
        },
    )

    category_id = create_response.json()["category_id"]

    response = client.delete(f"/categories/{category_id}")

    assert response.status_code == 204

    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404


def test_duplicate_category_returns_conflict(client):
    payload = {
        "category_name": "Groceries",
        "description": "Food items",
    }

    first_response = client.post("/categories", json=payload)
    second_response = client.post("/categories", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_missing_category_returns_not_found(client):
    response = client.get("/categories/99999")

    assert response.status_code == 404


def test_invalid_category_returns_validation_error(client):
    response = client.post(
        "/categories",
        json={
            "category_name": "",
            "description": "Invalid category",
        },
    )

    assert response.status_code == 422
