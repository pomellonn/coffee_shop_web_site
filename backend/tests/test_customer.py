import pytest

@pytest.mark.anyio
async def test_login_user(client):
    # Регистрация пользователя
    register_payload = {
        "email": "loginuser@example.com",
        "password": "loginpass123",
        "name": "Login User"
    }
    register_response = await client.post("/api/v1/users/register", json=register_payload)
    assert register_response.status_code == 201

    # Вход в систему
    login_payload = {
        "username": "loginuser@example.com",
        "password": "loginpass123"
    }
    login_response = await client.post("/api/v1/auth/token", data=login_payload)
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_for_access_token(client, customer_user):
    login_payload = {
        "username": "customer@example.com",
        "password": "custpass"
    }
    response = await client.post("/api/v1/auth/token", data=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.anyio
async def test_get_user_profile(client, token_headers_customer):
    # Получение профиля пользователя с токеном
    response = await client.get("/api/v1/users/me", headers=token_headers_customer)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert data["email"] == "customer@example.com"


@pytest.mark.anyio
async def test_update_user_profile(client, token_headers_customer):
    # Обновление имени пользователя
    payload = {"name": "Updated Customer"}
    response = await client.put("/api/v1/users/me", json=payload, headers=token_headers_customer)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Customer"


@pytest.mark.anyio
async def test_customer_cannot_access_manager_endpoints(client, token_headers_customer):
    # Клиент не должен иметь доступ к менеджерским эндпоинтам
    response = await client.get("/api/v1/manager/orders/", headers=token_headers_customer)
    assert response.status_code == 403


@pytest.mark.anyio
async def test_list_shops_and_get_shop(client, db_session, manager_user):
    # Должен вернуть список доступных кофеен и информацию о конкретной кофейне
    from sqlalchemy import select
    from app.models import CoffeeShop

    resp = await client.get("/api/v1/shops/")
    assert resp.status_code == 200
    shops = resp.json()
    assert isinstance(shops, list)
    assert len(shops) >= 1

    # Get shop id directly from DB (customer view doesn't expose shop_id)
    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    assert shop is not None

    resp2 = await client.get(f"/api/v1/shops/{shop.shop_id}")
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["name"] == shop.name
    assert data["address"] == shop.address


@pytest.mark.anyio
async def test_products_listing_and_get(client, create_product_factory):
    # Создаем продукт через фабрику и проверяем публичные эндпоинты
    p = await create_product_factory(
        name="Test Coffee",
        description="Tasty",
        image_url=None,
        volume=250,
        product_type="coffee",
        price=150,
    )

    r = await client.get("/api/v1/products/")
    assert r.status_code == 200
    all_products = r.json()
    assert any(prod["product_id"] == p.product_id for prod in all_products)

    r2 = await client.get(f"/api/v1/products/{p.product_id}")
    assert r2.status_code == 200
    prod = r2.json()
    assert prod["name"] == "Test Coffee"


@pytest.mark.anyio
async def test_shop_menu_and_sorting(client, db_session, manager_user, create_product_factory):
    # Prepare: create products and add them to the shop menu
    from sqlalchemy import select
    from app.models import ShopMenu, CoffeeShop

    p1 = await create_product_factory(
        name="A Coffee",
        description="A",
        image_url=None,
        volume=200,
        product_type="coffee",
        price=100,
    )
    p2 = await create_product_factory(
        name="B Coffee",
        description="B",
        image_url=None,
        volume=200,
        product_type="coffee",
        price=200,
    )

    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()

    # add menu entries
    m1 = ShopMenu(shop_id=shop.shop_id, product_id=p1.product_id, is_available=True)
    m2 = ShopMenu(shop_id=shop.shop_id, product_id=p2.product_id, is_available=True)
    db_session.add_all([m1, m2])
    await db_session.commit()

    r = await client.get(f"/api/v1/menu/{shop.shop_id}")
    assert r.status_code == 200
    menu = r.json()
    assert len(menu) >= 2

    r_asc = await client.get(f"/api/v1/menu/{shop.shop_id}/sorted-price-asc")
    assert r_asc.status_code == 200
    prices = [item["product"]["price"] for item in r_asc.json()]
    assert prices == sorted(prices)

    r_desc = await client.get(f"/api/v1/menu/{shop.shop_id}/sorted-price-desc")
    assert r_desc.status_code == 200
    prices_desc = [item["product"]["price"] for item in r_desc.json()]
    assert prices_desc == sorted(prices_desc, reverse=True)


@pytest.mark.anyio
async def test_create_order_and_get_my_orders(client, db_session, manager_user, token_headers_customer, create_product_factory):
    # Prepare shop, product and add to menu
    from sqlalchemy import select
    from app.models import ShopMenu, CoffeeShop

    p = await create_product_factory(
        name="Order Coffee",
        description="",
        image_url=None,
        volume=250,
        product_type="coffee",
        price=120,
    )
    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    m = ShopMenu(shop_id=shop.shop_id, product_id=p.product_id, is_available=True)
    db_session.add(m)
    await db_session.commit()

    order_payload = {"shop_id": shop.shop_id, "items": [{"product_id": p.product_id, "quantity": 2}]}
    resp = await client.post("/api/v1/orders/", json=order_payload, headers=token_headers_customer)
    assert resp.status_code == 201
    order = resp.json()
    assert order["total_amount"] == 240
    assert len(order["items"]) == 1

    resp2 = await client.get("/api/v1/orders/me", headers=token_headers_customer)
    assert resp2.status_code == 200
    orders = resp2.json()
    assert len(orders) >= 1


@pytest.mark.anyio
async def test_order_fails_if_product_not_in_shop(client, db_session, manager_user, token_headers_customer, create_product_factory):
    # Create a product but do not add to shop
    from sqlalchemy import select
    from app.models import CoffeeShop

    p = await create_product_factory(
        name="NotInShop",
        description="",
        image_url=None,
        volume=100,
        product_type="coffee",
        price=50,
    )
    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()

    order_payload = {"shop_id": shop.shop_id, "items": [{"product_id": p.product_id, "quantity": 1}]}
    resp = await client.post("/api/v1/orders/", json=order_payload, headers=token_headers_customer)
    # Debug on failure
    if resp.status_code != 400:
        print("ORDER_NOT_IN_SHOP FAILED:", await resp.aread())
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_order_fails_if_product_not_found(client, db_session, manager_user, token_headers_customer):
    # Product id does not exist - use shop id from DB
    from sqlalchemy import select
    from app.models import CoffeeShop
    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    assert shop is not None

    order_payload = {"shop_id": shop.shop_id, "items": [{"product_id": 99999, "quantity": 1}]}
    resp = await client.post("/api/v1/orders/", json=order_payload, headers=token_headers_customer)
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_customer_cannot_use_admin_endpoints_delete_user(client, token_headers_customer, customer_user):
    # Customer should not be able to delete other users via admin endpoint
    resp = await client.delete(f"/api/v1/admin/users/{customer_user.user_id}", headers=token_headers_customer)
    assert resp.status_code == 403