from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, Request
import hashlib
from pydantic import EmailStr
import string
import requests


from ..models import schemas, crud
from ..core.database import get_db
from ..core.config import settings
from ..core import utils
from ..core import oauth2
from ..core.oauth2 import AuthJWT


router = APIRouter()


@router.post(
    "/payment-transaction",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProfileResponseSchema,
)
async def transaction(
    profile: schemas.ProfileBaseSchema,
    db: Session = Depends(get_db),
    user_id=Depends(oauth2.require_user),
):
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



import requests

url = "http://v2.pepperest.com/EscrowBackend/api/ThirdParty/payment/createPayment"

payload = "{\n    \"buyer_name\": \"Yusuf Jamiu\",\n    \"buyer_email\": \"jamo@gmail.com\",\n    \"buyer_phone\": \"08123434371\",\n    \"description\": \"payment for Television\",\n    \"start_date\": \"2023-05-12\",\n    \"end_date\": \"2023-05-20\",\n    \"callback\": \"localhost:8000/verify-payment\",\n    \"cost\": \"10000\",\n    \"currency\": \"NGN\"\n}"
headers = {
  'Api-Key': 'peppa_MmGC9gq7JYXmHluLZ1LMEtkYEo6TGX4bmr3VefOXBoGEOHbdx49fKsCBzep7Z6dE'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
