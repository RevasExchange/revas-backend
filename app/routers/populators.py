from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..populators import locations, product
from ..models import crud
from ..models import crud


router = APIRouter()


@router.get("/populate-location", status_code=status.HTTP_200_OK)
async def populate_location(db: Session = Depends(get_db)):
    """
    Populates the location database with data.

    This function is an asynchronous route handler for the "/populate-location" endpoint. It takes a database session as a dependency and uses it to populate the location database with data.

    Parameters:
        - db (Session): The database session. Defaults to the result of the get_db function.

    Returns:
        - dict: A dictionary with a single key-value pair. The key is "status" and the value is "ok".
    """
    await locations.populate_db(db)
    return {"status": "Successfully populated the location database"}


@router.get("/populate-product", status_code=status.HTTP_200_OK)
async def populate_product(db: Session = Depends(get_db)):
    """
    Populates the product database with data.

    This function is an asynchronous route handler for the "/populate-product" endpoint. It takes a database session as a dependency and uses it to populate the product database with data.

    Parameters:
        - db (Session): The database session. Defaults to the result of the get_db function.

    Returns:
        - dict: A dictionary with a single key-value pair. The key is "status" and the value is "ok".
    """
    await product.populate_db(db)
    return {"status": "Successfully populated the product database"}
