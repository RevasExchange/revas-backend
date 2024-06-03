from datetime import datetime
from typing import Any
import uuid
from pydantic import BaseModel, EmailStr, constr


BaseModel.Config.arbitrary_types_allowed = True


class UserBaseSchema(BaseModel):
    firstname: str
    lastname: str
    companyemail: EmailStr
    companyname: str
    role: str


class VerifyEmailSchema(BaseModel):
    verificationtoken: str
    companyemail: EmailStr
    updatedat: datetime | None = None
    emailverified: bool | None = None


class ResendTokenSchema(BaseModel):
    companyemail: EmailStr


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
    companyemail: EmailStr
    password: constr(min_length=8)


class UserLoginResponseSchema(UserResponseSchema):
    access_token: str
    refresh_token: str


class ProfileBaseSchema(BaseModel):
    # company: str
    # business_email: EmailStr
    # position: str
    country_id: str
    state_id: str
    factory_capacity: int
    # products: list[str]
    products: str
    updatedat: datetime | None = None
    user_id: uuid.UUID | None = None

    # bio: str | None = None
    # website: str | None = None
    # profile_picture: str | None = None
    # profile_cover: str | None = None
    # location: str | None = None
    # social_links: list[str] | None = None
    # social_links_type: list[str] | None = None


class ProfileResponseSchema(ProfileBaseSchema):
    createdat: datetime

    class Config:
        orm_mode = True


class UpdateProfileSchema(ProfileBaseSchema):
    # position: str = None
    # country: str = None
    # factory_capacity: int = None
    # product: list[str] = None
    # updatedat: datetime = None

    # bio: str = None
    # website: str = None
    # profile_picture: str = None
    # profile_cover: str = None
    # location: str = None
    # social_links: list[str] = None
    # social_links_type: list[str] = None
    id: str


class WaitlistBaseSchema(BaseModel):
    workemail: EmailStr
    firstname: str
    lastname: str
    country_id: str
    state_id: str


class WaitlistResponseSchema(BaseModel):
    id: str

    class Config:
        orm_mode = True


class ProductBaseSchema(BaseModel):
    volume: str
    duration: str
    price: float
    destination: str
    paymentterms: str
    shippingterms: str
    location: str


class ProductResponseSchema(ProductBaseSchema):
    id: uuid.UUID
    user_id: uuid.UUID
    createdat: datetime
    updatedat: datetime

    class Config:
        orm_mode = True


class UpdateProductSchema(ProductBaseSchema):
    id: uuid.UUID


# class CreatePaymentSchema(BaseModel):
#     name: str
#     email: str
#     phone: str
#     description: str
#     start_date: datetime
#     end_date: datetime
#     callback: str
#     cost: str
#     currency: str


# class PaymentResponseSchema(BaseModel):
#     user_id: uuid.UUID
#     createdat: datetime

#     class Config:
#         orm_mode = True


# class PaymentBaseSchema(BaseModel):
#     name: str
