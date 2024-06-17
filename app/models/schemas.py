from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List


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
    # updatedat: datetime | None = None


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
    country_id: str
    state_id: str
    factory_capacity: int
    products: Optional[List[str]]
    # products: str
    # updatedat: datetime | None = None
    user_id: uuid.UUID | None = None
    # updatedat: datetime | None = None


class ProfileResponseSchema(ProfileBaseSchema):
    createdat: datetime
    updatedat: datetime
    id: uuid.UUID

    class Config:
        orm_mode = True


class UpdateProfileSchema(BaseModel):
    id: str
    country_id: str | None = None
    state_id: str | None = None
    factory_capacity: int | None = None
    products: Optional[List[str]] | None = None
    # products: str | None = None
    # updatedat: datetime | None = None


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
