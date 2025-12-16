from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from datetime import date, timedelta
from db.session import get_session
from core.security import get_current_user, require_manager
from models import Order, OrderItem, Product, CoffeeShop, User, UserRole


router_manager = APIRouter(
    prefix="/manager/analytics",
    tags=["Analytics - Manager"],
)


async def get_manager_shop(
    current_user: User = Depends(require_manager),
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        select(CoffeeShop).where(CoffeeShop.manager_id == current_user.user_id)
    )
    shop = result.scalars().first()

    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager has no assigned shop",
        )

    return shop


@router_manager.get("/")
async def get_manager_analytics(
    date_from: date = Query(...),
    date_to: date = Query(...),
    shop=Depends(get_manager_shop),
    db: AsyncSession = Depends(get_session),
):
    shop_id = shop.shop_id
    orders_stmt = select(
        func.date_trunc("day", Order.created_at).label("day"),
        func.count(Order.order_id).label("orders_count"),
    ).where(
        Order.created_at >= date_from, Order.created_at < date_to + timedelta(days=1)
    )
    if shop_id:
        orders_stmt = orders_stmt.where(Order.shop_id == shop_id)
    orders_stmt = orders_stmt.group_by("day").order_by("day")
    orders_result = await db.execute(orders_stmt)
    orders_per_day = [
        {"date": r.day.date(), "count_of_orders": r.orders_count} for r in orders_result
    ]
    # по месяцам
    months_stmt = select(
        func.to_char(func.date_trunc("month", Order.created_at), "YYYY-MM").label(
            "month"
        ),
        func.count(Order.order_id).label("orders_count"),
        func.sum(Order.total_amount).label("revenue"),
        func.avg(Order.total_amount).label("avg_check"),
    ).where(
        Order.created_at >= date_from, Order.created_at < date_to + timedelta(days=1)
    )
    months_stmt = months_stmt.group_by("month").order_by("month")
    months_result = await db.execute(months_stmt)
    monthly_summary = [
        {
            "month": r.month,
            "orders_count": r.orders_count,
            "revenue": float(r.revenue) if r.revenue else 0,
            "avg_check": float(r.avg_check) if r.avg_check else 0,
        }
        for r in months_result
    ]

    # Рейтинг продуктов
    products_stmt = (
        select(
            Product.name,
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
        )
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .join(Order, Order.order_id == OrderItem.order_id)
        .where(
            Order.created_at >= date_from,
            Order.created_at < date_to + timedelta(days=1),
        )
    )
    if shop_id:
        products_stmt = products_stmt.where(Order.shop_id == shop_id)
    products_stmt = products_stmt.group_by(Product.name).order_by(
        func.sum(OrderItem.quantity).desc()
    )
    products_result = await db.execute(products_stmt)
    product_ranking = [
        {"product": r.name, "total_sold": r.total_sold, "revenue": r.revenue}
        for r in products_result
    ]

    #  Продажи по времени суток
    time_stmt = select(
        case(
            (func.extract("hour", Order.created_at).between(8, 11), "Утро"),
            (func.extract("hour", Order.created_at).between(12, 16), "День"),
            else_="Вечер",
        ).label("time_period"),
        func.count(Order.order_id).label("orders_count"),
    ).where(
        Order.created_at >= date_from, Order.created_at < date_to + timedelta(days=1)
    )
    if shop_id:
        time_stmt = time_stmt.where(Order.shop_id == shop_id)

    time_stmt = time_stmt.group_by("time_period")
    time_result = await db.execute(time_stmt)

    time_period_sales = [
        {"period": r.time_period, "orders": r.orders_count} for r in time_result
    ]

    return {
        "shop_id": shop_id,
        "date_from": date_from,
        "date_to": date_to,
        "orders_per_day": orders_per_day,
        "monthly_summary": monthly_summary,
        "product_ranking": product_ranking,
        "time_period_sales": time_period_sales,
    }


router_admin = APIRouter(
    prefix="/admin/analytics",
    tags=["Analytics - Admin"],
)


# по выбранной кофейне
@router_admin.get("/shops/one")
async def get_one_shop_analytics(
    date_from: date = Query(..., description="YYYY-MM-DD"),
    date_to: date = Query(..., description="YYYY-MM-DD"),
    shop_id: int | None = Query(None, description="ID кофейни (только для админа)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    # shop_id depends on manager
    if current_user.role == UserRole.manager:
        if not current_user.shop_id:
            raise HTTPException(status_code=400, detail="Manager has no shop")
        shop_id = current_user.shop_id

    elif current_user.role == UserRole.admin:
        if shop_id is None:
            raise HTTPException(
                status_code=400,
                detail="shop_id is required for admin",
            )

    else:
        raise HTTPException(status_code=403, detail="Access denied")
    # Количество заказов по дням
    orders_stmt = select(
        func.date_trunc("day", Order.created_at).label("day"),
        func.count(Order.order_id).label("orders_count"),
    ).where(
        Order.created_at >= date_from, Order.created_at < date_to + timedelta(days=1)
    )
    if shop_id:
        orders_stmt = orders_stmt.where(Order.shop_id == shop_id)
    orders_stmt = orders_stmt.group_by("day").order_by("day")
    orders_result = await db.execute(orders_stmt)
    orders_per_day = [
        {"date": r.day.date(), "count_of_orders": r.orders_count} for r in orders_result
    ]
    # по месяцам
    months_stmt = select(
        func.to_char(func.date_trunc("month", Order.created_at), "YYYY-MM").label(
            "month"
        ),
        func.count(Order.order_id).label("orders_count"),
        func.sum(Order.total_amount).label("revenue"),
        func.avg(Order.total_amount).label("avg_check"),
    ).where(
        Order.created_at >= date_from, Order.created_at < date_to + timedelta(days=1)
    )
    months_stmt = months_stmt.group_by("month").order_by("month")
    months_result = await db.execute(months_stmt)
    monthly_summary = [
        {
            "month": r.month,
            "orders_count": r.orders_count,
            "revenue": float(r.revenue) if r.revenue else 0,
            "avg_check": float(r.avg_check) if r.avg_check else 0,
        }
        for r in months_result
    ]

    # Рейтинг продуктов
    products_stmt = (
        select(
            Product.name,
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
        )
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .join(Order, Order.order_id == OrderItem.order_id)
        .where(
            Order.created_at >= date_from,
            Order.created_at < date_to + timedelta(days=1),
        )
    )
    if shop_id:
        products_stmt = products_stmt.where(Order.shop_id == shop_id)
    products_stmt = products_stmt.group_by(Product.name).order_by(
        func.sum(OrderItem.quantity).desc()
    )
    products_result = await db.execute(products_stmt)
    product_ranking = [
        {"product": r.name, "total_sold": r.total_sold, "revenue": r.revenue}
        for r in products_result
    ]

    #  Продажи по времени суток
    time_stmt = select(
        case(
            (func.extract("hour", Order.created_at).between(8, 11), "Утро"),
            (func.extract("hour", Order.created_at).between(12, 16), "День"),
            else_="Вечер",
        ).label("time_period"),
        func.count(Order.order_id).label("orders_count"),
    ).where(
        Order.created_at >= date_from, Order.created_at < date_to + timedelta(days=1)
    )
    if shop_id:
        time_stmt = time_stmt.where(Order.shop_id == shop_id)

    time_stmt = time_stmt.group_by("time_period")
    time_result = await db.execute(time_stmt)

    time_period_sales = [
        {"period": r.time_period, "orders": r.orders_count} for r in time_result
    ]

    return {
        "shop_id": shop_id,
        "date_from": date_from,
        "date_to": date_to,
        "orders_per_day": orders_per_day,
        "monthly_summary": monthly_summary,
        "product_ranking": product_ranking,
        "time_period_sales": time_period_sales,
    }


# По всем кофейням


@router_admin.get("/shops/all")
async def get_full_analytics(
    date_from: date = Query(..., description="Start date, format YYYY-MM-DD"),
    date_to: date = Query(..., description="End date, format YYYY-MM-DD"),
    db: AsyncSession = Depends(get_session),
):
    # Количество заказов по дням
    orders_stmt = select(
        func.date_trunc("day", Order.created_at).label("day"),
        func.count(Order.order_id).label("orders_count"),
    ).where(
        Order.created_at >= date_from, Order.created_at < date_to + timedelta(days=1)
    )

    orders_stmt = orders_stmt.group_by("day").order_by("day")
    orders_result = await db.execute(orders_stmt)
    orders_per_day = [
        {"date": r.day.date(), "count_of_orders": r.orders_count} for r in orders_result
    ]

    # по месяцам
    months_stmt = select(
        func.to_char(func.date_trunc("month", Order.created_at), "YYYY-MM").label(
            "month"
        ),
        func.count(Order.order_id).label("orders_count"),
        func.sum(Order.total_amount).label("revenue"),
        func.avg(Order.total_amount).label("avg_check"),
    ).where(
        Order.created_at >= date_from, Order.created_at < date_to + timedelta(days=1)
    )
    months_stmt = months_stmt.group_by("month").order_by("month")
    months_result = await db.execute(months_stmt)
    monthly_summary = [
        {
            "month": r.month,
            "orders_count": r.orders_count,
            "revenue": float(r.revenue) if r.revenue else 0,
            "avg_check": float(r.avg_check) if r.avg_check else 0,
        }
        for r in months_result
    ]

    # Рейтинг продуктов
    products_stmt = (
        select(
            Product.name,
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue"),
        )
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .join(Order, Order.order_id == OrderItem.order_id)
        .where(
            Order.created_at >= date_from,
            Order.created_at < date_to + timedelta(days=1),
        )
    )

    products_stmt = products_stmt.group_by(Product.name).order_by(
        func.sum(OrderItem.quantity).desc()
    )
    products_result = await db.execute(products_stmt)
    product_ranking = [
        {"product": r.name, "total_sold": r.total_sold, "revenue": r.revenue}
        for r in products_result
    ]

    # Продажи по времени суток
    time_stmt = (
        select(
            CoffeeShop.name,
            case(
                (func.extract("hour", Order.created_at).between(8, 11), "Утро"),
                (func.extract("hour", Order.created_at).between(12, 16), "День"),
                else_="Вечер",
            ).label("time_period"),
            func.count(Order.order_id).label("orders_count"),
        )
        .where(
            Order.created_at >= date_from,
            Order.created_at < date_to + timedelta(days=1),
        )
        .group_by(CoffeeShop.name)
    )

    time_stmt = time_stmt.group_by("time_period")
    time_result = await db.execute(time_stmt)
    time_period_sales = [
        {"Coffee_shop": r.name, "period": r.time_period, "orders": r.orders_count}
        for r in time_result
    ]

    # Средний чек и количество заказов в кофейне
    shops_stmt = (
        select(
            CoffeeShop.name,
            func.avg(Order.total_amount).label("avg_check"),
            func.count(Order.order_id).label("orders_count"),
            func.sum(Order.total_amount).label("total_revenue"),
        )
        .join(Order, CoffeeShop.shop_id == Order.shop_id)
        .where(
            Order.created_at >= date_from,
            Order.created_at < date_to + timedelta(days=1),
        )
        .group_by(CoffeeShop.name)
        .order_by(func.avg(Order.total_amount))
    )
    shops_result = await db.execute(shops_stmt)
    shops_summary = [
        {
            "shop": r.name,
            "avg_check": float(r.avg_check),
            "orders_count": r.orders_count,
            "total_revenue": float(r.total_revenue),
        }
        for r in shops_result
    ]

    return {
        "date_from": date_from,
        "date_to": date_to,
        "orders_per_day": orders_per_day,
        "monthly_summary": monthly_summary,
        "product_ranking": product_ranking,
        "time_period_sales": time_period_sales,
        "shops_summary": shops_summary,
    }


# клиенты


@router_admin.get("/clients/top")
async def get_clients_analytics(
    date_from: date = Query(..., description="Start date, format YYYY-MM-DD"),
    date_to: date = Query(..., description="End date, format YYYY-MM-DD"),
    db: AsyncSession = Depends(get_session),
):
    clients_stmt = (
        select(
            User.email,
            func.count(Order.order_id).label("total_purchases"),
            func.sum(Order.total_amount).label("spent_money"),
            func.count(func.distinct(Order.shop_id)).label("shops_visited"),
        )
        .join(Order, User.user_id == Order.user_id)
        .where(
            User.role == "customer",
            Order.created_at >= date_from,
            Order.created_at < date_to + timedelta(days=1),
        )
        .group_by(User.email)
        .order_by(func.count(Order.order_id).desc())
        .limit(20)
    )
    clients_result = await db.execute(clients_stmt)
    top_clients = [
        {
            "email": r.email,
            "total_purchases": r.total_purchases,
            "spent_money": float(r.spent_money),
            "shops_visited": r.shops_visited,
        }
        for r in clients_result
    ]
    return {"date_from": date_from, "date_to": date_to, "top_clients": top_clients}


@router_admin.get("/clients/stats")
async def get_clients_stats(
    date_from: date = Query(..., description="Start date, format YYYY-MM-DD"),
    date_to: date = Query(..., description="End date, format YYYY-MM-DD"),
    db: AsyncSession = Depends(get_session),
):

    subq = (
        select(Order.user_id, func.count(Order.order_id).label("orders_count"))
        .where(
            Order.created_at >= date_from,
            Order.created_at < date_to + timedelta(days=1),
        )
        .group_by(Order.user_id)
        .subquery()
    )

    stats_stmt = select(
        func.count().filter(subq.c.orders_count == 1).label("one_time"),
        func.count().filter(subq.c.orders_count > 1).label("returning"),
    )

    result = await db.execute(stats_stmt)
    row = result.first()

    return {"one_time": row.one_time, "returning": row.returning}
