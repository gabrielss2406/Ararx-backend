from typing import Union

from starlette import status
from starlette.exceptions import HTTPException

from api.dependencies import get_password_hash
from api.models.UsersModels import UserIn, UserOut
from api.services.db import connect_mongo


def create_user(user: UserIn) -> Union[UserOut, None]:
    collection, client = connect_mongo('Users')
    user.password = get_password_hash(user.password)

    try:
        email_check = collection.find_one({"email": user.email})
        if email_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f" user with email '{user.email}' already exists!"
            )

        handler_check = collection.find_one({"handler": user.handler})
        if handler_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f" user with handler '{user.handler}' already exists!"
            )

        user = UserOut(**user.dict())

        result = collection.insert_one(user.to_pymongo())
        if result.acknowledged:
            return user
    except Exception as e:
        raise e
