from datetime import datetime
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response, Request
from random import choices
from pydantic import EmailStr
import string


from ..models import schemas, crud
from ..core.database import get_db
from ..core.config import settings
from ..core import utils
from ..core.oauth2 import AuthJWT


from ..mailHandler.email import Email


OTP_Length = 6
router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponseSchema,
)
async def signup(
    user: schemas.CreateUserSchema, request: Request, db: Session = Depends(get_db)
):
    """
    Handle user signup with validation, hashing of password, and sending verification email.

    Args:
        user (schemas.CreateUserSchema): The user data to be created.
        request (Request): The request object for the HTTP request.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.UserResponseSchema: The newly created user data.
    """
    try:
        user_exists = await crud.get_user_by_email(db, email=user.companyemail)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
            )

        hashed_password = utils.hash_password(user.password)
        user.password = hashed_password.decode("utf-8")
        user.companyemail = user.companyemail.lower()

        try:
            otp = "".join(choices(string.digits, k=OTP_Length))
            user.verificationtoken = otp
            try:
                await crud.create_user(db, user)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"{e}: Error creating user in the db",
                )

            await Email(
                user=user.lastname, token=otp, email=[EmailStr(user.companyemail)]
            ).sendVerificationEmail()

            new_user = await crud.get_user_by_email(db, email=user.companyemail)
            return new_user

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}: There was an error sending verification mail",
            )

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}: Error creating user",
        )


@router.post("/verify-email", status_code=status.HTTP_204_NO_CONTENT)
async def verify_email(
    verification_data: schemas.VerifyEmailSchema, db: Session = Depends(get_db)
):
    """
    Function for verifying email using verification token.

    Args:
        verification_data (schemas.VerifyEmailSchema): The verification data including email and verification token.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If there's an error updating the user or if the OTP is invalid.
        HTTPException: If there's an internal server error during the verification process.

    Returns:
        dict: A dictionary with the status and message of the verification process.
    """
    try:
        user = await crud.get_user_by_email(db, email=verification_data.companyemail)
        if (
            user is not None
            and user.verificationtoken == verification_data.verificationtoken
        ):
            verification_data.emailverified = True
            verification_data.verificationtoken = None
            verification_data.updatedat = datetime.utcnow()
            result = await crud.update_email_verified(db, verification_data)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Error updating user (Invalid verifivation token or User does not exist)",
                )

            else:
                return {"status": "Success", "message": "Account Verified Successfully"}

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid OTP"
            )

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}: Error verifying email",
        )


@router.post("/resend-token", status_code=status.HTTP_204_NO_CONTENT)
async def resend_token(user: schemas.ResendTokenSchema, db: Session = Depends(get_db)):
    """
    A function to resend a token to the user for verification.

    Args:
        user: A schema representing the user details for resending the token.
        db: A database session dependency.

    Returns:
        If successful, returns a dictionary with status and message indicating successful token sent.
        If unsuccessful, raises an HTTPException with the appropriate status code and error detail.
    """
    try:
        user_exists = await crud.get_user_by_email(db, email=user.companyemail)
        if user_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{e}: User does not exist",
            )

        otp = "".join(choices(string.digits, k=OTP_Length))
        user_exists.verificationtoken = otp
        user_exists.updatedat = datetime.utcnow()
        result = await crud.update_user(db, user_exists)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{e}: Error updating user (Invalid verifivation token or User does not exist)",
            )

        else:
            await Email(
                user=user_exists.lastname,
                token=otp,
                email=[EmailStr(user_exists.companyemail)],
            ).sendVerificationEmail()

            return {"status": "Success", "message": "Token Sent Successfully"}

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}: Error sending token to mail",
        )


@router.post(
    "/login",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.UserLoginResponseSchema,
)
async def login(
    login_data: schemas.UserLoginSchema,
    response: Response,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    """
    Handles the user login process. Verifies the user's credentials, creates access and refresh tokens, sets cookies, and updates the user's access and refresh tokens.
    Parameters:
    - login_data: UserLoginSchema - the user's login data
    - response: Response - the HTTP response object
    - db: Session = Depends(get_db) - the database session
    - Authorize: AuthJWT = Depends() - the authorization object
    Returns:
    - UserLoginResponseSchema - the user login response schema
    """
    try:
        user_exist = await crud.get_user_by_email(db, email=login_data.companyemail)
        if not user_exist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Credentials (User does not exist)",
            )

        if user_exist:
            password = login_data.password
            if utils.verify_password(password, user_exist.password):
                access_token = Authorize.create_access_token(
                    subject=str(user_exist.id),
                    expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                )
                refresh_token = Authorize.create_refresh_token(
                    subject=str(user_exist.id),
                    expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
                )

                response.set_cookie(
                    "access_token",
                    access_token,
                    ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    "/",
                    None,
                    False,
                    True,
                    "lax",
                )

                response.set_cookie(
                    "refresh_token",
                    refresh_token,
                    ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    "/",
                    None,
                    False,
                    True,
                    "lax",
                )

                response.set_cookie(
                    "logged_in",
                    "True",
                    ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    "/",
                    None,
                    False,
                    False,
                    "lax",
                )

                user_exist.access_token = access_token
                user_exist.refresh_token = refresh_token

                # return {
                #     "access_token": access_token,
                #     # "refresh_token": refresh_token,
                #     "data": user_exist,
                # }
                return user_exist

            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid password",
                )

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}: Error logging in",
        )


@router.get("/refresh-token", status_code=status.HTTP_202_ACCEPTED)
async def refresh(
    response: Response, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)
):
    """
    A function to refresh the access token, with parameters response: Response, Authorize: AuthJWT, db: Session, and a return type of dictionary.
    """
    try:
        Authorize.jwt_refresh_token_required()

        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(
            subject=current_user, expires_time=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        response.set_cookie(
            "access_token",
            new_access_token,
            ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "/",
            None,
            False,
            True,
            "lax",
        )

        response.set_cookie(
            "logged_in",
            "True",
            ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "/",
            None,
            False,
            False,
            "lax",
        )

        return {"access_token": new_access_token}

    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}: Error refreshing token",
        )


@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends()):
    """
    Logout route to unset the JWT cookies and clear the 'logged_in' cookie.

    Parameters:
    - response: Response - the response object for the HTTP request
    - Authorize: AuthJWT - the JWT authorization dependency

    Returns:
    - dict: A dictionary with the status of the operation
    """
    Authorize.unset_jwt_cookies()
    response.set_cookie("logged_in", "", -1)

    return {"status": "success"}
