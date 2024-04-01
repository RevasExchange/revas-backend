from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, Request
import hashlib
from random import randbytes, choices
from pydantic import EmailStr
import string


from ..models import schemas, crud
from ..core.database import get_db
from ..core.config import settings
from ..core import utils
from ..core import oauth2
from ..core.oauth2 import AuthJWT


router = APIRouter()


@router.post(
    "/create-profile",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProfileResponseSchema,
)
async def create_profile(
    profile: schemas.ProfileBaseSchema,
    db: Session = Depends(get_db),
    user_id=Depends(oauth2.require_user),
):
    """
    Function to create a profile with the given profile data for the specified user.
    Parameters:
        - profile: A schema representing the profile data to be created.
        - db: A database session dependency.
        - user_id: A user ID obtained from the OAuth2 authentication.
    Returns:
        - The created profile response schema.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            profile.user_id = user_id
            result = await crud.create_profile(db, profile)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"{e}: Profile creation failed",
                )

            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}: User not Found"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}: Profile creation failed (Internal Server Error)",
        )


@router.patch(
    "/edit-profile",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ProfileResponseSchema,
)
async def update_state(
    updateonboard: schemas.UpdateProfileSchema,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.require_user),
):
    """
    Updates the state of the user's onboarding profile.

    Parameters:
        - updateonboard (schemas.UpdateProfileSchema): The updated profile information.
        - db (Session, optional): The database session. Defaults to Depends(get_db).
        - user_id (str, optional): The user ID. Defaults to Depends(oauth2.require_user).

    Returns:
        - schemas.ProfileResponseSchema: The updated profile response.

    Raises:
        - HTTPException: If the user is not found or if there is a bad request.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            result = await crud.edit_profile(
                db=db, customer_id=user.id, updated_onboard=updateonboard
            )

            return result

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/get-profile",
    status_code=status.HTTP_200_OK,
)
async def get_state(
    db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)
):
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            result = await crud.get_profile(db=db, user_id=user.id)

            if result:
                return result
            else:
                return {"data": {"value": False}}

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}: Profile editing failed (Internal Server Error)",
        )


@router.delete(
    "/delete-profile",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_profile(
    db: Session = Depends(get_db), user_id: str = Depends(oauth2.require_user)
):
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            result = await crud.delete_profile(db=db, user_id=user.id)

            if result:
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}: Profile deletion failed (Internal Server Error)",
        )
