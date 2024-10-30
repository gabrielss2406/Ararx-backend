import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import APIRouter
from starlette import status
from starlette.exceptions import HTTPException

from api.dependencies import create_access_token
from api.models.UsersModels import UserIn
from api.models.structural.TokenModels import Token
from api.services.user.create import create_user

router = APIRouter(prefix="/register", tags=["register"])

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


@router.post("/", response_model=Token, summary="Register one user")
def register_student(user: UserIn) -> Token:
    try:
        result = create_user(user)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user.email} or handler {user.handler} already exists!",
            )

        user = result

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.handler}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise e
