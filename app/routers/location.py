from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..locations import locations
from ..models import crud


router = APIRouter()


@router.get("/populate-location", status_code=status.HTTP_200_OK)
async def populate_location(db: Session = Depends(get_db)):
    await locations.populate_db(db)
    return {"status": "ok"}


@router.get("/countries", status_code=status.HTTP_200_OK)
async def get_countries(db: Session = Depends(get_db)):
    return await crud.get_countries(db)


@router.get("/states", status_code=status.HTTP_200_OK)
async def get_states(country_id: str, db: Session = Depends(get_db)):
    return await crud.get_states(db, country_id=country_id)
