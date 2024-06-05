import base64
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from .config import settings
from ..models import crud
from .database import get_db
from sqlalchemy.orm import Session


class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {"cookies", "headers"}
    authjwt_access_cookie_key: str = "access_token"
    authjwt_refresh_cookie_key: str = "refresh_token"
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(settings.JWT_PUBLIC_KEY).decode("utf-8")
    authjwt_private_key: str = base64.b64decode(settings.JWT_PRIVATE_KEY).decode(
        "utf-8"
    )
    # authjwt_public_key: str = settings.JWT_PUBLIC_KEY
    # authjwt_private_key: str = settings.JWT_PRIVATE_KEY


@AuthJWT.load_config
def get_config():
    """
    A function that loads the configuration for AuthJWT.

    Returns:
        Settings: An instance of the Settings class that contains the configuration settings for AuthJWT.
    """
    return Settings()


class NotVerified(Exception):
    pass


class UserNotFound(Exception):
    pass


async def require_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    Asynchronously retrieves a user from the database based on the provided JWT token.

    :param db: The database session. Defaults to the result of the `get_db` dependency.
    :type db: Session
    :param Authorize: The AuthJWT dependency. Defaults to the result of the `AuthJWT` dependency.
    :type Authorize: AuthJWT

    :raises HTTPException 401: If the user belonging to the token no longer exists, the token is invalid or has expired, or the user has not verified their account.

    :return: The ID of the user.
    :rtype: int
    """
    try:
        Authorize.jwt_refresh_token_required()
        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not refresh access token",
            )
        user = await crud.get_user(db, user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The user belonging to this token no logger exist",
            )

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == "MissingTokenError":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in"
            )
        if error == "UserNotFound":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exist"
            )
        if error == "NotVerified":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please verify your account",
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or has expired",
        )

    return user.id
