import base64
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


from .config import settings
from ..models import crud
from .database import get_db
from sqlalchemy.orm import Session


# class Settings(BaseModel):
#     authjwt_algorithm: str = settings.JWT_ALGORITHM
#     authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
#     authjwt_token_location: set = {"cookies", "headers"}
#     authjwt_access_cookie_key: str = "access_token"
#     authjwt_refresh_cookie_key: str = "refresh_token"
#     authjwt_cookie_csrf_protect: bool = False
#     authjwt_public_key: str = base64.b64decode(settings.JWT_PUBLIC_KEY).decode("utf-8")
#     authjwt_private_key: str = base64.b64decode(settings.JWT_PRIVATE_KEY).decode(
#         "utf-8"
#     )


class Settings(BaseModel):
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [settings.JWT_ALGORITHM]
    authjwt_token_location: set = {"cookies", "headers"}
    authjwt_access_cookie_key: str = "access_token"
    authjwt_refresh_cookie_key: str = "refresh_token"
    authjwt_cookie_csrf_protect: bool = False

    # Decode base64 encoded keys
    try:
        authjwt_public_key: str = base64.b64decode(
            settings.JWT_PUBLIC_KEY + "=" * ((4 - len(settings.JWT_PUBLIC_KEY) % 4) % 4)
        ).decode("utf-8")
        authjwt_private_key: str = base64.b64decode(
            settings.JWT_PRIVATE_KEY
            + "=" * ((4 - len(settings.JWT_PRIVATE_KEY) % 4) % 4)
        ).decode("utf-8")
    except base64.binascii.Error as e:
        # Handle decoding errors
        print("Error decoding base64 string:", e)
        authjwt_public_key = ""
        authjwt_private_key = ""


@AuthJWT.load_config
def get_config():
    """
    Load the config for the AuthJWT and return the Settings object.
    """
    return Settings()


async def require_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    An asynchronous function that requires a user to be authenticated.
    It takes in a database session and an authentication object as parameters.
    It first checks if the user is authenticated using the provided JWT, and then retrieves the current user.
    If the user is not found or is not authenticated, it raises an HTTPException. It returns the ID of the authenticated user.
    """
    try:
        # Authorize.jwt_required()
        # Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
            )

        user = crud.get_user(db, current_user)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist"
            )

    except Exception as e:
        error = e.__class__.__name__
        if error == "MissingTokenError":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing access token (Please Login)",
            )
        if error == "UserNotFound":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
            )
        if error == "NotVerified":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not verified"
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return user.id
