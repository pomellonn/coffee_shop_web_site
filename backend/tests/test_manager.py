import pytest


@pytest.mark.anyio
async def test_manager_get_my_shop(client, manager_user, token_headers_manager):
    resp = await client.get("/api/v1/manager/shops/info", headers=token_headers_manager)
    assert resp.status_code == 200
    data = resp.json()
    assert data["manager_id"] == manager_user.user_id


@pytest.mark.anyio
async def test_manager_cannot_access_admin_shops(client, token_headers_manager):
    resp = await client.get("/api/v1/admin/shops/", headers=token_headers_manager)
    assert resp.status_code == 403


@pytest.mark.anyio
async def test_manager_create_menu_item_and_list(
    client, db_session, manager_user, token_headers_manager, create_product_factory
):
    from sqlalchemy import select
    from app.models import CoffeeShop, ShopMenu

    # create product
    p = await create_product_factory(
        name="Mgr Coffee",
        description="",
        image_url=None,
        volume=200,
        product_type="coffee",
        price=99,
    )

    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()

    payload = {"product_id": p.product_id, "is_available": True}
    resp = await client.post(
        "/api/v1/manager/menu/", json=payload, headers=token_headers_manager
    )
    assert resp.status_code == 201
    item = resp.json()
    assert item["product"]["product_id"] == p.product_id

    # list manager menu
    resp2 = await client.get("/api/v1/manager/menu/", headers=token_headers_manager)
    assert resp2.status_code == 200
    items = resp2.json()
    assert any(i["shop_id"] == shop.shop_id for i in items)


@pytest.mark.anyio
async def test_manager_update_menu_item_and_delete(
    client, db_session, manager_user, token_headers_manager, create_product_factory
):
    from sqlalchemy import select
    from app.models import CoffeeShop, ShopMenu

    p = await create_product_factory(
        name="To Update",
        description="",
        image_url=None,
        volume=200,
        product_type="coffee",
        price=150,
    )

    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    m = ShopMenu(shop_id=shop.shop_id, product_id=p.product_id, is_available=True)
    db_session.add(m)
    await db_session.commit()

    # update availability
    payload = {"is_available": False}
    resp = await client.put(
        f"/api/v1/manager/menu/{m.shop_menu_id}",
        json=payload,
        headers=token_headers_manager,
    )
    assert resp.status_code == 200
    assert resp.json()["is_available"] is False

    # delete
    resp2 = await client.delete(
        f"/api/v1/manager/menu/{m.shop_menu_id}", headers=token_headers_manager
    )
    assert resp2.status_code == 204


@pytest.mark.anyio
async def test_manager_get_orders_and_count(
    client, db_session, manager_user, token_headers_manager, create_product_factory
):
    from sqlalchemy import select
    from app.models import CoffeeShop, ShopMenu, Product, Order, OrderItem

    # create product and add to shop menu and create an order for the shop
    p = await create_product_factory(
        name="Order Mgr",
        description="",
        image_url=None,
        volume=200,
        product_type="coffee",
        price=50,
    )

    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    m = ShopMenu(shop_id=shop.shop_id, product_id=p.product_id, is_available=True)
    db_session.add(m)
    await db_session.commit()

    order = Order(user_id=manager_user.user_id, shop_id=shop.shop_id, total_amount=100)
    oi = OrderItem(product_id=p.product_id, unit_price=50, quantity=2)
    order.items = [oi]
    db_session.add(order)
    await db_session.commit()

    # get orders for my shop
    resp = await client.get("/api/v1/manager/orders/", headers=token_headers_manager)
    assert resp.status_code == 200
    orders = resp.json()
    assert any(o["shop_id"] == shop.shop_id for o in orders)

    # orders count
    resp2 = await client.get(
        "/api/v1/manager/orders/orders-count", headers=token_headers_manager
    )
    assert resp2.status_code == 200
    data = resp2.json()
    assert "count" in data


@pytest.mark.anyio
async def test_manager_create_product_allowed(client, token_headers_manager):

    payload = {
        "name": "MgrProduct",
        "description": "",
        "image_url": None,
        "volume": 250,
        "product_type": "coffee",
        "price": 120,
    }
    resp = await client.post(
        "/api/v1/admin/products/", json=payload, headers=token_headers_manager
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "MgrProduct"


@pytest.mark.anyio
async def test_manager_cannot_delete_product(
    client, token_headers_manager, db_session, create_product_factory
):
    p = await create_product_factory(
        name="DelProd",
        description="",
        image_url=None,
        volume=120,
        product_type="coffee",
        price=50,
    )

    resp = await client.delete(
        f"/api/v1/admin/products/{p.product_id}", headers=token_headers_manager
    )
    assert resp.status_code == 204
