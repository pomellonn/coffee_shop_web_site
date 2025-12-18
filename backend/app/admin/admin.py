from sqladmin import ModelView, expose, BaseView
from fastapi import Request
from sqlalchemy import func, select
from app.db.session import SessionLocal
from app.models import Order
from app.models import User, CoffeeShop, Product, Order
from app.db.session import AsyncSessionLocal
import httpx
from app.core.config import settings
from fastapi.responses import HTMLResponse


class UserAdmin(ModelView, model=User):
    column_list = [User.user_id, User.email, User.name, User.role]


class CoffeeShopAdmin(ModelView, model=CoffeeShop):
    column_list = [
        CoffeeShop.shop_id,
        CoffeeShop.name,
        CoffeeShop.address,
        CoffeeShop.manager_id,
    ]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.product_id,
        Product.name,
        Product.product_type,
        Product.price,
    ]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.order_id, Order.user_id, Order.shop_id, Order.total_amount]



class AnalyticsOneShopView(BaseView):
    name = "Анализ по одной кофейне"
    icon = "fa fa-chart-bar"
    identity = "oneshop" 

    @expose("/oneshop", methods=["GET"])
    async def analytics_one(self, request: Request):
        return await self.templates.TemplateResponse(
            request,
            "admin/oneshop_analytics.html",
            context={"request": request}
        )



class AnalyticsAllShopsView(BaseView):
    name = "Анализ по всем кофейням"
    icon = "fa fa-chart-bar"
    identity = "allshops" 

    @expose("/allshops", methods=["GET"])
    async def analytics_all(self, request: Request):
        return await self.templates.TemplateResponse(
            request,
            "admin/allshops_analytics.html",
            context={"request": request}
        )

class AnalyticsClientsView(BaseView):
    name = "Анализ клиентов кофеен"
    icon = "fa fa-chart-bar"
    identity = "clients" 

    @expose("/clients", methods=["GET"])
    async def analytics_page(self, request: Request):
        return await self.templates.TemplateResponse(
            request,
            "admin/clients_analytics.html",
            context={"request": request}
        )

