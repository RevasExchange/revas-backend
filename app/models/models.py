import uuid
from ..core.database import Base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    TIMESTAMP,
    Boolean,
    Numeric,
    Integer,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY
import datetime


def current_time():
    """
    Returns the current UTC time.

    This function uses the `datetime.datetime.utcnow()` method to get the current UTC time.

    Returns:
        datetime.datetime: The current UTC time.
    """
    return datetime.datetime.utcnow()


class User(Base):
    __tablename__ = "users"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    companyname = Column(String(255), nullable=False)
    companyemail = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phonenumber = Column(String(255), nullable=False, unique=True)
    createdat = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    updatedat = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=current_time,
        onupdate=current_time,
    )
    verificationtoken = Column(String(255), nullable=True)
    emailverified = Column(Boolean, nullable=False, default=False)
    # profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User")
    createdat = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    updatedat = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=current_time,
        onupdate=current_time,
    )
    country_id = Column(String(255), ForeignKey("country.id"), nullable=False)
    country = relationship("Country")
    state_id = Column(String(255), ForeignKey("state.id"), nullable=False)
    state = relationship("State")
    factory_capacity = Column(Numeric, nullable=False)
    products = Column(String(255), nullable=False)
    # products = Column(ARRAY(String), nullable=False)


class Payment(Base):
    __tablename__ = "payment"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User")
    createdat = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    updatedat = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=current_time,
        onupdate=current_time,
    )
    cost = Column(Numeric, nullable=False)
    currency = Column(String(255), nullable=False)
    callback = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)


class Product(Base):
    __tablename__ = "product"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User")
    createdat = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    updatedat = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=current_time,
        onupdate=current_time,
    )
    volume = Column(String(255), nullable=False)
    duration = Column(String(255), nullable=False)
    price = Column(Numeric, nullable=False)
    destination = Column(String(255), nullable=False)
    paymentterms = Column(String(255), nullable=False)
    shippingterms = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)


class Country(Base):
    __tablename__ = "country"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    alpha_2 = Column(String(255), nullable=False, unique=True)
    alpha_3 = Column(String(255), nullable=False, unique=True)


class State(Base):
    __tablename__ = "state"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    country_id = Column(String(255), ForeignKey("country.id"), nullable=False)
    country = relationship("Country")


class AllProducts(Base):
    __tablename__ = "allproducts"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False, unique=True)
    createdat = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
    updatedat = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=current_time,
        onupdate=current_time,
    )


class Waitlist(Base):
    __tablename__ = "waitlist"
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workemail = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    country_id = Column(String(255), ForeignKey("country.id"), nullable=False)
    country = relationship("Country")
    state_id = Column(String(255), ForeignKey("state.id"), nullable=False)
    state = relationship("State")
    createdat = Column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.datetime.utcnow
    )
