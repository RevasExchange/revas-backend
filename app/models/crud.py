from sqlalchemy.orm import Session
from pydantic import EmailStr
from datetime import datetime
import json


from ..models import models, schemas


async def get_user(db: Session, user_id: str):
    """
    Asynchronously retrieves a user from the database based on the provided user_id.

    Parameters:
    - db: The database session
    - user_id: The unique identifier of the user

    Returns:
    - The user object from the database, or None if not found
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(db: Session, email: EmailStr):
    """
    Asynchronous function to retrieve a user from the database by email.

    Args:
        db (Session): The database session.
        email (EmailStr): The email address of the user.

    Returns:
        models.User: The user corresponding to the given email, or None if not found.
    """
    return db.query(models.User).filter(models.User.email == email).first()


# async def get_users(db: Session, skip: int = 0, limit: int = 100):
#     """
#     Asynchronous function to retrieve users from the database.

#     Args:
#         db (Session): The database session.
#         skip (int, optional): Number of records to skip. Defaults to 0.
#         limit (int, optional): Maximum number of records to retrieve. Defaults to 100.

#     Returns:
#         List[User]: List of user objects retrieved from the database.
#     """
#     return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: schemas.CreateUserSchema):
    """
    Asynchronously creates a new user in the database.

    Parameters:
    - db: Session object representing the database session
    - user: CreateUserSchema object containing the user information to be created

    Returns:
    - User object representing the newly created user
    """
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def update_user(db: Session, user: schemas.UpdateUserSchema):
    """
    Asynchronously updates a user in the database.

    Args:
        db (Session): The database session.
        user (schemas.UpdateUserSchema): The updated user information.

    Returns:
        models.User: The updated user if successful, None otherwise.
    """
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return None


async def delete_user(db: Session, user_id: str):
    """
    An asynchronous function to delete a user from the database.

    Parameters:
    - db: A database session object.
    - user_id: An integer representing the user's ID.

    Returns:
    - True if the user was successfully deleted, False otherwise.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    else:
        return False


async def update_email_verified(db: Session, user: schemas.VerifyEmailSchema):
    """
    An asynchronous function to update the email verification status of a user in the database.

    Args:
        db (Session): The database session.
        user (schemas.VerifyEmailSchema): The user data to update the email verification status.

    Returns:
        models.User: The updated user if found, otherwise None.
    """
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        return None


# async def update_password(db: Session, user: schemas.UpdatePasswordSchema):
#     """
#     An asynchronous function to update the password of a user in the database.

#     Args:
#         db (Session): The database session.
#         user (schemas.UpdatePasswordSchema): The user data to update the password.

#     Returns:
#         models.User: The updated user if found, otherwise None.
#     """
#     db_user = db.query(models.User).filter(models.User.email == user.email).first()
#     if db_user:
#         for key, value in user.dict(exclude_unset=True).items():
#             setattr(db_user, key, value)
#         db.commit()
#         db.refresh(db_user)
#         return db_user
#     else:
#         return None


async def create_profile(db: Session, profile: schemas.ProfileBaseSchema):
    """
    An asynchronous function to create a new profile in the database.

    Args:
        db (Session): The database session.
        profile (schemas.ProfileBaseSchema): The profile data to be created.

    Returns:CreateProfileSchema
        models.Profile: The newly created profile object.
    """
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


async def edit_profile(db: Session, user_id: str, profile: schemas.UpdateProfileSchema):
    """
    An asynchronous function to update an existing profile in the database.

    Args:
        db (Session): The database session.
        profile (schemas.UpdateProfileSchema): The profile data to be updated.

    Returns:
        models.Profile: The updated profile object if found, otherwise None.
    """
    db_profile = (
        db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    )
    if db_profile:
        for key, value in profile.dict(exclude_unset=True).items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
        return db_profile
    else:
        return None


async def get_profile(db: Session, user_id: str):
    """
    An asynchronous function to retrieve a profile from the database.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user whose profile is being retrieved.

    Returns:
        models.Profile: The profile object if found, otherwise None.
    """
    return db.query(models.Profile).filter(models.Profile.user_id == user_id).first()


# async def get_profiles(db: Session, skip: int = 0, limit: int = 100):
#     """
#     An asynchronous function to retrieve all profiles from the database.

#     Args:
#         db (Session): The database session.
#         skip (int, optional): Number of records to skip. Defaults to 0.
#         limit (int, optional): Maximum number of records to retrieve. Defaults to 100.

#     Returns:
#         List[Profile]: List of profile objects retrieved from the database.
#     """
#     return db.query(models.Profile).offset(skip).limit(limit).all()


async def delete_profile(db: Session, user_id: str):
    """
    An asynchronous function to delete a profile from the database.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user whose profile is being deleted.

    Returns:
        bool: True if the profile was successfully deleted, False otherwise.
    """
    db_profile = (
        db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    )
    if db_profile:
        db.delete(db_profile)
        db.commit()
        return True
    else:
        return False