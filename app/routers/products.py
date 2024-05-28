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
    "/product",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProductResponseSchema,
)
async def create_product(
    product: schemas.ProductBaseSchema,
    db: Session = Depends(get_db),
    user_id=Depends(oauth2.require_user),
):
    """
    Creates a new product in the database.

    Parameters:
        - product (schemas.ProductBaseSchema): The data of the product to be created.
        - db (Session, optional): The database session. Defaults to the session obtained from `get_db` dependency.
        - user_id (str, optional): The ID of the user. Defaults to the user ID obtained from the `oauth2.require_user` dependency.

    Returns:
        - schemas.ProductResponseSchema: The created product.

    Raises:
        - HTTPException: If the user is not found or the product creation fails.

    Notes:
        - This function is an asynchronous function.
        - The response model is `schemas.ProductResponseSchema`.
        - The status code of the response is `status.HTTP_201_CREATED`.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            product.user_id = user_id
            result = await crud.create_product(db, product)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"{e}: Product creation failed",
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
            detail=f"{e}: Product creation failed (Internal Server Error)",
        )


@router.patch(
    "/product",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ProductResponseSchema,
)
async def update_product(
    updateproduct: schemas.UpdateProductSchema,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.require_user),
):
    """
    Updates a product in the database.

    Parameters:
        - updateproduct (schemas.UpdateProductSchema): The data of the product to be updated.
        - db (Session, optional): The database session. Defaults to the session obtained from `get_db` dependency.
        - user_id (str, optional): The ID of the user. Defaults to the user ID obtained from the `oauth2.require_user` dependency.

    Returns:
        - schemas.ProductResponseSchema: The updated product.

    Raises:
        - HTTPException: If the product is not found or the update fails.

    Notes:
        - This function is an asynchronous function.
        - The response model is `schemas.ProductResponseSchema`.
        - The status code of the response is `status.HTTP_200_OK`.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            product = await crud.get_product(db, product_id=updateproduct.id)

            if product:
                result = await crud.edit_product(
                    db=db, user_id=user_id, product=updateproduct
                )

                return result

            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
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
            detail=f"{e}: Product update failed (Internal Server Error)",
        )


@router.get(
    "/product",
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.require_user),
):
    """
    Retrieves a product from the database based on the provided product ID.

    Args:
        product_id (str): The ID of the product to retrieve.
        db (Session, optional): The database session. Defaults to the session obtained from `get_db` dependency.
        user_id (str, optional): The ID of the user. Defaults to the user ID obtained from the `oauth2.require_user` dependency.

    Returns:
        Union[schemas.ProductResponseSchema, HTTPException]: The retrieved product if found, or an HTTPException with a 404 status code if the product or user is not found.

    Raises:
        HTTPException: If an error occurs during the retrieval process, an HTTPException with a 400 status code is raised, indicating an internal server error.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            result = await crud.get_product(db=db, product_id=product_id)

            if result:
                return result
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
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
            detail=f"{e}: Product fetch failed (Internal Server Error)",
        )


@router.get(
    "/all-product",
    status_code=status.HTTP_200_OK,
)
async def get_all_product(
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.require_user),
):
    """
    Retrieves all products from the database.

    Parameters:
        - db (Session, optional): The database session. Defaults to the session obtained from `get_db` dependency.
        - user_id (str, optional): The ID of the user. Defaults to the user ID obtained from the `oauth2.require_user` dependency.

    Returns:
        - List[schemas.ProductResponseSchema]: A list of products if found, or an HTTPException with a 404 status code if the products or user is not found.

    Raises:
        - HTTPException: If an error occurs during the retrieval process, an HTTPException with a 400 status code is raised, indicating an internal server error.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            result = await crud.get_products(db=db)

            if result:
                return result
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Products not found"
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
            detail=f"{e}: Product fetch failed (Internal Server Error)",
        )


@router.delete(
    "/delete-profile",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_profile(
    product_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(oauth2.require_user),
):
    """
    Deletes a profile from the database.

    Args:
        product_id (str): The ID of the product to be deleted.
        db (Session, optional): The database session. Defaults to the session obtained from the `get_db` dependency.
        user_id (str, optional): The ID of the user who owns the profile. Defaults to the user ID obtained from the `oauth2.require_user` dependency.

    Raises:
        HTTPException: If the user or product is not found.
        HTTPException: If the product deletion fails.

    Returns:
        Response: An empty response with a status code of 204 if the profile is successfully deleted.
    """
    try:
        user = await crud.get_user(db, user_id=user_id)

        if user:
            product = await crud.get_product(db, product_id=product_id)

            if product:
                result = await crud.delete_product(
                    db=db, product_id=product_id, user_id=user_id
                )

                if result:
                    return Response(status_code=status.HTTP_204_NO_CONTENT)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Unable to delete product",
                    )

            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
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
            detail=f"{e}: Product deletion failed (Internal Server Error)",
        )
