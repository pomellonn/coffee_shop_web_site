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
 
        "product_type": "coffee",
        "price": 100,
    }
    resp = await client.post("/api/v1/admin/products/", json=payload)
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_admin_shop_crud_and_permissions(
    client, token_headers_admin, token_headers_manager
):

    payload = {"name": "Admin Shop", "address": "Admin Address"}
    resp = await client.post(
        "/api/v1/admin/shops/", json=payload, headers=token_headers_admin
    )
    assert resp.status_code == 201
    shop = resp.json()
    assert shop["name"] == payload["name"]
    assert "shop_id" in shop

    sid = shop["shop_id"]

    resp = await client.get("/api/v1/admin/shops/", headers=token_headers_admin)
    assert resp.status_code == 200
    shops = resp.json()
    assert any(s["shop_id"] == sid for s in shops)

    resp = await client.get(f"/api/v1/admin/shops/{sid}", headers=token_headers_admin)
    assert resp.status_code == 200
    s = resp.json()
    assert s["shop_id"] == sid

    update = {"name": "Updated Admin Shop"}
    resp = await client.put(
        f"/api/v1/admin/shops/{sid}", json=update, headers=token_headers_admin
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["name"] == update["name"]

    resp = await client.get("/api/v1/admin/shops/", headers=token_headers_manager)
    assert resp.status_code == 403

    resp = await client.delete(
        f"/api/v1/admin/shops/{sid}", headers=token_headers_admin
    )
    assert resp.status_code == 204

    resp = await client.get(f"/api/v1/admin/shops/{sid}", headers=token_headers_admin)
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_admin_menu_crud_and_list(
    client, token_headers_admin, create_product_factory
):

    product = await create_product_factory(
        name="Menu Product",
        description="",
        image_url=None,
   
        product_type="coffee",
        price=50,
    )

    shop_resp = await client.post(
        "/api/v1/admin/shops/",
        json={"name": "Shop For Menu", "address": "Addr"},
        headers=token_headers_admin,
    )
    assert shop_resp.status_code == 201
    shop = shop_resp.json()
    sid = shop["shop_id"]

    payload = {"shop_id": sid, "product_id": product.product_id, "is_available": True}
    resp = await client.post(
        "/api/v1/admin/menu/", json=payload, headers=token_headers_admin
    )
    assert resp.status_code == 201
    item = resp.json()
    assert item["shop_id"] == sid
    assert item["product"]["product_id"] == product.product_id

    mid = item["shop_menu_id"]

    resp = await client.get("/api/v1/admin/menu/", headers=token_headers_admin)
    assert resp.status_code == 200
    all_items = resp.json()
    assert any(i["shop_menu_id"] == mid for i in all_items)

    resp = await client.put(
        f"/api/v1/admin/menu/{mid}",
        json={"is_available": False},
        headers=token_headers_admin,
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["is_available"] is False

    resp = await client.delete(f"/api/v1/admin/menu/{mid}", headers=token_headers_admin)
    assert resp.status_code == 204

    resp = await client.get("/api/v1/admin/menu/", headers=token_headers_admin)
    assert resp.status_code == 200
    assert all(i["shop_menu_id"] != mid for i in resp.json())


from datetime import date, timedelta


@pytest.mark.anyio
async def test_admin_orders_and_analytics(
    client, token_headers_admin, token_headers_customer, create_product_factory
):
    shop_resp = await client.post(
        "/api/v1/admin/shops/",
        json={"name": "Shop For Orders", "address": "Addr"},
        headers=token_headers_admin,
    )
    assert shop_resp.status_code == 201
    shop = shop_resp.json()
    sid = shop["shop_id"]

    product = await create_product_factory(
        name="Order Product",
        description="",
        image_url=None,
  
        product_type="coffee",
        price=150,
    )

    resp = await client.post(
        "/api/v1/admin/menu/",
        json={"shop_id": sid, "product_id": product.product_id, "is_available": True},
        headers=token_headers_admin,
    )
    assert resp.status_code == 201

    order_payload = {
        "shop_id": sid,
        "items": [{"product_id": product.product_id, "quantity": 1}],
    }
    resp = await client.post(
        "/api/v1/orders/", json=order_payload, headers=token_headers_customer
    )
    assert resp.status_code == 201
    order = resp.json()
    assert order["shop_id"] == sid
    oid = order["order_id"]

    resp = await client.get("/api/v1/admin/orders/", headers=token_headers_admin)
    assert resp.status_code == 200
    orders = resp.json()
    assert any(o["order_id"] == oid for o in orders)

    today = date.today()
    date_from = (today - timedelta(days=1)).isoformat()
    date_to = today.isoformat()

    resp = await client.get(
        f"/api/v1/admin/analytics/shops/one?date_from={date_from}&date_to={date_to}",
        headers=token_headers_admin,
    )
    assert resp.status_code == 400

    resp = await client.get(
        f"/api/v1/admin/analytics/shops/one?date_from={date_from}&date_to={date_to}&shop_id={sid}",
        headers=token_headers_admin,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["shop_id"] == sid
    assert "orders_per_day" in data
    assert "monthly_summary" in data
    assert "product_ranking" in data

    resp = await client.get(
        f"/api/v1/admin/analytics/shops/all?date_from={date_from}&date_to={date_to}",
        headers=token_headers_admin,
    )
    assert resp.status_code == 200
    full = resp.json()
    assert "orders_per_day" in full
    assert "monthly_summary" in full

    resp = await client.get(
        f"/api/v1/admin/analytics/clients/top?date_from={date_from}&date_to={date_to}",
        headers=token_headers_admin,
    )
    assert resp.status_code == 200
    top = resp.json()
    assert "top_clients" in top

    resp = await client.get(
        f"/api/v1/admin/analytics/clients/stats?date_from={date_from}&date_to={date_to}",
        headers=token_headers_admin,
    )
    assert resp.status_code == 200
    stats = resp.json()
    assert "one_time" in stats and "returning" in stats
