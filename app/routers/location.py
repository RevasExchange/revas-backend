from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..locations import locations
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


@router.get("/countries", status_code=status.HTTP_200_OK)
async def get_countries(db: Session = Depends(get_db)):
    """
    Asynchronously retrieves a list of countries from the database.

    Parameters:
    - db (Session, optional): The database session. Defaults to the result of the get_db function.

    Returns:
    - A list of country objects from the database.
    """
    return await crud.get_countries(db)


@router.get("/states", status_code=status.HTTP_200_OK)
async def get_states(country_id: str, db: Session = Depends(get_db)):
    """
    Asynchronously retrieves a list of states from the database based on the provided country ID.

    Parameters:
    - country_id (str): The ID of the country for which states are being retrieved.
    - db (Session, optional): The database session. Defaults to the result of the get_db function.

    Returns:
    - A list of state objects from the database that belong to the specified country.
    """
    return await crud.get_states(db, country_id=country_id)
