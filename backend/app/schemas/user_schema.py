from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from models import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email address of the user")
    name: str = Field(..., min_length=1, max_length=50, description="Name of the user")
    model_config = ConfigDict(from_attributes=True)


# Create schema - Customer View
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password for the user")
    model_config = ConfigDict(from_attributes=True)


# Create schema - Admin View
class UserCreateAdmin(UserCreate):
    role: UserRole = Field(..., description="Role of the user in the system")
    model_config = ConfigDict(from_attributes=True)


# Read schema - Customer View
class UserReadCustomer(UserBase):
    model_config = ConfigDict(from_attributes=True)


# Read schema - Manager/Admin View
class UserReadManagerAdmin(UserBase):
    user_id: int
    role: UserRole = Field(..., description="Role of the user in the system")
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Update schema - Customer View
class UserUpdateCustomer(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# Update schema - Admin View
class UserUpdateAdmin(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[UserRole] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserWithToken(BaseModel):
    user: UserReadCustomer  # todo: UserReadManagerAdmin
    token: Token
    model_config = ConfigDict(from_attributes=True)
