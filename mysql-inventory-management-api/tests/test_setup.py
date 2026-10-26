def test_api_starts(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200


def test_test_database_has_expected_tables(db_session):
    table_names = set(
        db_session.get_bind().dialect.get_table_names(db_session.get_bind().connect())
    )

    assert {
        "categories",
        "products",
        "suppliers",
        "file_metadata",
    }.issubset(table_names)
