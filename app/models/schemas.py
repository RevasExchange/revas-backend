from datetime import datetime
from typing import Any
import uuid
from pydantic import BaseModel, EmailStr, constr


BaseModel.Config.arbitrary_types_allowed = True


class UserBaseSchema(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class VerifyEmailSchema(BaseModel):
    verificationtoken: str
    email: EmailStr
    updatedat: datetime | None = None
    emailverified: bool | None = None


class ResendTokenSchema(BaseModel):
    email: EmailStr


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    verificationtoken: str | None = None
    phonenumber: str
    updatedat: datetime | None = None


class UserResponseSchema(UserBaseSchema):
    id: uuid.UUID
    phonenumber: str
    updatedat: datetime
    createdat: datetime
    emailverified: bool = False

    class Config:
        orm_mode = True


class UpdateUserSchema(UserBaseSchema):
    phonenumber: str | None = None
    password: constr(min_length=8) | None = None
    updatedat: datetime | None = None
    verificationtoken: str | None = None
    emailverified: bool | None = None


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserLoginResponseSchema(UserResponseSchema):
    access_token: str
    refresh_token: str


class ProfileBaseSchema(BaseModel):
    company: str
    business_email: EmailStr
    position: str
    country: str
    factory_capacity: int
    product: list[str]
    updatedat: datetime | None = None

    bio: str | None = None
    website: str | None = None
    profile_picture: str | None = None
    profile_cover: str | None = None
    location: str | None = None
    social_links: list[str] | None = None
    social_links_type: list[str] | None = None


class ProfileResponseSchema(ProfileBaseSchema):
    user_id: uuid.UUID
    createdat: datetime

    class Config:
        orm_mode = True


class UpdateProfileSchema(BaseModel):
    position: str = None
    country: str = None
    factory_capacity: int = None
    product: list[str] = None
    updatedat: datetime = None

    bio: str = None
    website: str = None
    profile_picture: str = None
    profile_cover: str = None
    location: str = None
    social_links: list[str] = None
    social_links_type: list[str] = None


class CreatePaymentSchema(BaseModel):
    name: str
    email: str
    phone: str
    description: str
    start_date: datetime
    end_date: datetime
    callback: str
    cost: str
    currency: str


class PaymentResponseSchema(BaseModel):
    user_id: uuid.UUID
    createdat: datetime

    class Config:
        orm_mode = True


class PaymentBaseSchema(BaseModel):
    name: str