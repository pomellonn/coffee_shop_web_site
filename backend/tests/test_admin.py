import pytest


@pytest.mark.anyio
async def test_admin_create_user_and_list(client, db_session, token_headers_admin):
    payload = {
        "email": "newmanager@example.com",
        "name": "New Manager",
        "password": "securepass",
        "role": "manager",
    }
    resp = await client.post(
        "/api/v1/admin/users/", json=payload, headers=token_headers_admin
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == payload["email"]
    assert data["role"] == "manager"
    assert "user_id" in data
    resp = await client.get("/api/v1/admin/users/", headers=token_headers_admin)
    assert resp.status_code == 200
    users = resp.json()
    assert any(u["email"] == payload["email"] for u in users)


@pytest.mark.anyio
async def test_admin_endpoint_forbidden_for_manager(client, token_headers_manager):
    payload = {
        "email": "another@example.com",
        "name": "Another",
        "password": "securepass",
        "role": "customer",
    }
    resp = await client.post(
        "/api/v1/admin/users/", json=payload, headers=token_headers_manager
    )
    assert resp.status_code == 403


@pytest.mark.anyio
async def test_admin_product_crud(client, token_headers_admin):
    # Create product
    payload = {
        "name": "Admin Coffee",
        "description": "Admin special",
        "image_url": None,
        "volume": 250,
        "product_type": "coffee",
        "price": 199,
    }
    resp = await client.post(
        "/api/v1/admin/products/", json=payload, headers=token_headers_admin
    )
    assert resp.status_code == 201
    product = resp.json()
    assert product["name"] == payload["name"]
    assert "product_id" in product

    pid = product["product_id"]

    update = {"price": 249}
    resp = await client.put(
        f"/api/v1/admin/products/{pid}", json=update, headers=token_headers_admin
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["price"] == 249

    resp = await client.delete(
        f"/api/v1/admin/products/{pid}", headers=token_headers_admin
    )
    assert resp.status_code == 204

    resp = await client.get(f"/api/v1/products/{pid}")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_admin_product_requires_auth(client):
    payload = {
        "name": "NoAuth Coffee",
        "description": "",
        "image_url": None,
        "volume": 200,
        "product_type": "coffee",
        "price": 100,
    }
    resp = await client.post("/api/v1/admin/products/", json=payload)
    assert resp.status_code == 401
