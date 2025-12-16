from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy.orm import Session

from db.session import SessionLocal
from models import User
from core.config import settings
from core.security import verify_password
SECRET_KEY = settings.SECRET_KEY


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(User.email == username).first()

            if not user:
                return False

            if user and verify_password(password, user.password_hash) and user.role.value == "admin":
                request.session["admin_user"] = user.user_id
                return True

            if user.role != "admin":
                return False

            request.session["admin_user"] = user.email
            return True
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return "admin_user" in request.session


authentication_backend = AdminAuth(secret_key=SECRET_KEY)