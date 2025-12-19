import pytest
from sqlalchemy import select


@pytest.mark.anyio
async def test_create_order_with_options_customer(
    client, db_session, token_headers_customer, create_product_factory, manager_user
):
    from app.models import (
        AttributeType,
        ProductAttributeOptions,
        ProductAttributes,
        ShopMenu,
        CoffeeShop,
    )

    p = await create_product_factory(
        name="Option Coffee",
        description="",
        image_url=None,
        product_type="coffee",
        price=100,
    )

    at = AttributeType(attribute_name="size")
    db_session.add(at)
    await db_session.commit()
    await db_session.refresh(at)

    opt_small = ProductAttributeOptions(
        attribute_type_id=at.attribute_type_id, value="small", extra_price=-10
    )
    opt_large = ProductAttributeOptions(
        attribute_type_id=at.attribute_type_id, value="large", extra_price=20
    )
    db_session.add_all([opt_small, opt_large])
    await db_session.commit()
    await db_session.refresh(opt_small)
    await db_session.refresh(opt_large)

    # Link option_large to product
    pa = ProductAttributes(product_id=p.product_id, option_id=opt_large.option_id)
    db_session.add(pa)
    await db_session.commit()

    # Make product available in shop
    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    m = ShopMenu(shop_id=shop.shop_id, product_id=p.product_id, is_available=True)
    db_session.add(m)
    await db_session.commit()

    # Create order selecting the large size option
    order_payload = {
        "shop_id": shop.shop_id,
        "items": [
            {
                "product_id": p.product_id,
                "quantity": 1,
                "option_ids": [opt_large.option_id],
            }
        ],
    }
    resp = await client.post(
        "/api/v1/orders/", json=order_payload, headers=token_headers_customer
    )
    assert resp.status_code == 201, await resp.aread()
    order = resp.json()
    assert order["total_amount"] == 120
    assert len(order["items"]) == 1
    item = order["items"][0]
    assert item["unit_price"] == 120
    assert len(item["selected_options"]) == 1
    sel = item["selected_options"][0]
    assert sel["option_id"] == opt_large.option_id
    assert sel["attribute_type"] == "size"
    assert sel["value"] == "large"
    assert sel["extra_price"] == 20


@pytest.mark.anyio
async def test_create_order_invalid_option_customer(
    client, db_session, token_headers_customer, create_product_factory, manager_user
):
    from app.models import (
        AttributeType,
        ProductAttributeOptions,
        ShopMenu,
        CoffeeShop,
    )

    p = await create_product_factory(
        name="NoOpt Coffee",
        description="",
        image_url=None,
        product_type="coffee",
        price=100,
    )

    at = AttributeType(attribute_name="milk")
    db_session.add(at)
    await db_session.commit()
    await db_session.refresh(at)

    opt = ProductAttributeOptions(
        attribute_type_id=at.attribute_type_id, value="soy", extra_price=10
    )
    db_session.add(opt)
    await db_session.commit()
    await db_session.refresh(opt)

    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    m = ShopMenu(shop_id=shop.shop_id, product_id=p.product_id, is_available=True)
    db_session.add(m)
    await db_session.commit()

    order_payload = {
        "shop_id": shop.shop_id,
        "items": [
            {"product_id": p.product_id, "quantity": 1, "option_ids": [opt.option_id]}
        ],
    }
    resp = await client.post(
        "/api/v1/orders/", json=order_payload, headers=token_headers_customer
    )
    assert resp.status_code == 400
    assert "invalid for this product" in (await resp.aread()).decode()


@pytest.mark.anyio
async def test_manager_create_order_with_options(
    client, db_session, token_headers_manager, manager_user, create_product_factory
):
    from app.models import (
        AttributeType,
        ProductAttributeOptions,
        ProductAttributes,
        ShopMenu,
        CoffeeShop,
        User,
    )

    p = await create_product_factory(
        name="Manager Coffee",
        description="",
        image_url=None,
        product_type="coffee",
        price=80,
    )

    at = AttributeType(attribute_name="syrup")
    db_session.add(at)
    await db_session.commit()
    await db_session.refresh(at)

    opt = ProductAttributeOptions(
        attribute_type_id=at.attribute_type_id, value="vanilla", extra_price=15
    )
    db_session.add(opt)
    await db_session.commit()
    await db_session.refresh(opt)

    pa = ProductAttributes(product_id=p.product_id, option_id=opt.option_id)
    db_session.add(pa)
    await db_session.commit()

    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    m = ShopMenu(shop_id=shop.shop_id, product_id=p.product_id, is_available=True)
    db_session.add(m)
    await db_session.commit()

    customer = User(
        email="cust@example.com", password_hash="pwd", name="Cust", role="customer"
    )
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)

    order_payload = {
        "shop_id": shop.shop_id,
        "user_id": customer.user_id,
        "items": [
            {"product_id": p.product_id, "quantity": 2, "option_ids": [opt.option_id]}
        ],
    }
    resp = await client.post(
        "/api/v1/manager/orders/", json=order_payload, headers=token_headers_manager
    )
    assert resp.status_code == 201, await resp.aread()
    order = resp.json()
    assert order["total_amount"] == (80 + 15) * 2
    item = order["items"][0]
    assert item["unit_price"] == 95
    assert len(item["selected_options"]) == 1


@pytest.mark.anyio
async def test_admin_create_order_with_options(
    client, db_session, token_headers_admin, manager_user, create_product_factory
):
    from app.models import (
        AttributeType,
        ProductAttributeOptions,
        ProductAttributes,
        ShopMenu,
        CoffeeShop,
        User,
    )

    p = await create_product_factory(
        name="Admin Coffee",
        description="",
        image_url=None,
        product_type="coffee",
        price=90,
    )

    at = AttributeType(attribute_name="roast")
    db_session.add(at)
    await db_session.commit()
    await db_session.refresh(at)

    opt = ProductAttributeOptions(
        attribute_type_id=at.attribute_type_id, value="dark", extra_price=5
    )
    db_session.add(opt)
    await db_session.commit()
    await db_session.refresh(opt)

    pa = ProductAttributes(product_id=p.product_id, option_id=opt.option_id)
    db_session.add(pa)
    await db_session.commit()

    shop = (await db_session.execute(select(CoffeeShop))).scalars().first()
    m = ShopMenu(shop_id=shop.shop_id, product_id=p.product_id, is_available=True)
    db_session.add(m)
    await db_session.commit()

    customer = User(
        email="admincust@example.com",
        password_hash="pwd",
        name="Admin Cust",
        role="customer",
    )
    db_session.add(customer)
    await db_session.commit()
    await db_session.refresh(customer)

    order_payload = {
        "shop_id": shop.shop_id,
        "user_id": customer.user_id,
        "items": [
            {"product_id": p.product_id, "quantity": 1, "option_ids": [opt.option_id]}
        ],
    }
    resp = await client.post(
        "/api/v1/admin/orders/", json=order_payload, headers=token_headers_admin
    )
    assert resp.status_code == 201, await resp.aread()
    order = resp.json()
    assert order["total_amount"] == 95
    item = order["items"][0]
    assert item["unit_price"] == 95
    assert len(item["selected_options"]) == 1
