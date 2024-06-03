from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response


from ..models import schemas, crud
from ..core.database import get_db
from ..core import oauth2


router = APIRouter()


@router.post(
    "/profile",
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
            check_profile = await crud.get_profile_by_user(db, user_id=user_id)

            if check_profile:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Profile already exists",
                )

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

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}: Profile creation failed (Internal Server Error)",
        )


@router.patch(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ProfileResponseSchema,
)
async def update_profile(
    updateprofile: schemas.UpdateProfileSchema,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.require_user),
):
    """
    Updates the profile of a user.

    Parameters:
        updateprofile (schemas.UpdateProfileSchema): The updated profile data.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user_id (str, optional): The ID of the user. Defaults to Depends(oauth2.require_user).

    Returns:
        schemas.ProfileResponseSchema: The updated profile response.

    Raises:
        HTTPException: If the user or profile is not found.
        HTTPException: If there is an internal server error.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            profile = await crud.get_profile(db, profile_id=updateprofile.id)
            print("This is profile", profile.id)

            if profile:
                print("got here")
                result = await crud.edit_profile(
                    db=db, user_id=user_id, profile=updateprofile
                )

                return result

            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}: Profile update failed (Internal Server Error)",
        )


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
)
async def get_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.require_user),
):
    """
    An asynchronous function to retrieve a profile from the database.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user whose profile is being retrieved.

    Returns:
        Union[schemas.ProfileResponseSchema, Dict[str, Dict[str, bool]]]: The profile object if found, otherwise a dictionary with a "data" key containing a "value" key set to False.

    Raises:
        HTTPException: If the user is not found or if there is a bad request.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            result = await crud.get_profile(db=db, profile_id=profile_id)

            if result:
                return result
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}: Profile fetching failed (Internal Server Error)",
        )


@router.delete(
    "/profile",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_profile(
    profile_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.require_user),
):
    """
    Deletes a user's profile from the database.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user_id (str, optional): The ID of the user whose profile is being deleted. Defaults to Depends(oauth2.require_user).

    Raises:
        HTTPException: If the user is not found or if there is an internal server error during profile deletion.

    Returns:
        Response: An empty response with a status code of 204 if the profile was successfully deleted.
        HTTPException: A 404 Not Found error if the user is not found.
        HTTPException: A 400 Bad Request error if there was an error during profile deletion.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            profile = await crud.get_profile(db, profile_id=user.profile_id)

            if profile:
                result = await crud.delete_profile(
                    db=db, profile_id=profile_id, user_id=user.id
                )

                if result:
                    return Response(status_code=status.HTTP_204_NO_CONTENT)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Unable to delete profile",
                    )

            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found"
                )

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}: Profile deletion failed (Internal Server Error)",
        )
