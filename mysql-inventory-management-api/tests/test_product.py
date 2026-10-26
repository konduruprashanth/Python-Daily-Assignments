from unittest.mock import patch


def create_product_payload(category_id, supplier_id, **overrides):
    payload = {
        "product_name": "Test Laptop",
        "description": "Laptop for automated testing",
        "category_id": category_id,
        "supplier_id": supplier_id,
        "price": "750.00",
        "quantity": 25,
        "sku": "TEST-LAPTOP-001",
        "reorder_level": 5,
    }
    payload.update(overrides)
    return payload


def test_create_product(client, test_category, test_supplier):
    payload = create_product_payload(
        test_category.category_id,
        test_supplier.supplier_id,
    )

    # Prevent sending a real email during this test.
    with patch("app.services.product_service.send_low_stock_alert"):
        response = client.post("/products", json=payload)

    assert response.status_code == 201
    assert response.json()["product_name"] == "Test Laptop"
    assert response.json()["sku"] == "TEST-LAPTOP-001"
    assert response.json()["quantity"] == 25


def test_list_products(client, test_category, test_supplier):
    payload = create_product_payload(
        test_category.category_id,
        test_supplier.supplier_id,
    )
    response = client.post("/products", json=payload)

    assert response.status_code == 201

    list_response = client.get("/products")

    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1
    assert len(list_response.json()["items"]) == 1


def test_get_product(client, test_category, test_supplier):
    payload = create_product_payload(
        test_category.category_id,
        test_supplier.supplier_id,
    )
    create_response = client.post("/products", json=payload)
    product_id = create_response.json()["product_id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json()["product_id"] == product_id


def test_update_product(client, test_category, test_supplier):
    payload = create_product_payload(
        test_category.category_id,
        test_supplier.supplier_id,
    )
    create_response = client.post("/products", json=payload)
    product_id = create_response.json()["product_id"]

    with patch("app.services.product_service.send_low_stock_alert"):
        response = client.put(
            f"/products/{product_id}",
            json={"product_name": "Updated Test Laptop", "quantity": 20},
        )

    assert response.status_code == 200
    assert response.json()["product_name"] == "Updated Test Laptop"
    assert response.json()["quantity"] == 20


def test_delete_product(client, test_category, test_supplier):
    payload = create_product_payload(
        test_category.category_id,
        test_supplier.supplier_id,
    )
    create_response = client.post("/products", json=payload)
    product_id = create_response.json()["product_id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 204
    assert client.get(f"/products/{product_id}").status_code == 404


def test_duplicate_sku_returns_conflict(client, test_category, test_supplier):
    payload = create_product_payload(
        test_category.category_id,
        test_supplier.supplier_id,
    )

    first_response = client.post("/products", json=payload)
    second_response = client.post("/products", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_missing_product_returns_not_found(client):
    response = client.get("/products/99999")

    assert response.status_code == 404


def test_invalid_product_returns_validation_error(
    client,
    test_category,
    test_supplier,
):
    payload = create_product_payload(
        test_category.category_id,
        test_supplier.supplier_id,
        price="0",
    )

    response = client.post("/products", json=payload)

    assert response.status_code == 422


def test_product_pagination(client, test_category, test_supplier):
    for index in range(3):
        payload = create_product_payload(
            test_category.category_id,
            test_supplier.supplier_id,
            product_name=f"Test Product {index}",
            sku=f"TEST-PRODUCT-{index:03d}",
        )
        response = client.post("/products", json=payload)
        assert response.status_code == 201

    response = client.get("/products?page=1&page_size=2")

    assert response.status_code == 200
    assert len(response.json()["items"]) == 2
    assert response.json()["total"] == 3
