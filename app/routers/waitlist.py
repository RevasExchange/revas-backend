from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import EmailStr


from ..models import schemas, crud
from ..core.database import get_db
from ..mailHandler.waitlistmail import Email

router = APIRouter()


@router.post(
    "/waitlist",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.WaitlistResponseSchema,
)
async def create_waitlist(
    waitlist: schemas.WaitlistBaseSchema,
    db: Session = Depends(get_db),
):
    try:
        user_exists = await crud.get_waitlist_by_email(db, workemail=waitlist.workemail)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email Already Waitlisted"
            )

        try:
            await crud.create_waitlist_user(db, waitlist)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}: Error creating waitlist user in the db",
            )

        await Email(
            user=waitlist.lastname, email=[EmailStr(waitlist.workemail)]
        ).sendWaitlistEmail()

        new_user = await crud.get_waitlist_by_email(db, workemail=waitlist.workemail)
        return new_user

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}: Waitlist creation failed (Internal Server Error)",
        )
