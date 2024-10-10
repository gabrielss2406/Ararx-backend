from typing import Union

from starlette import status
from starlette.exceptions import HTTPException

import api.api
from api.dependencies import get_password_hash
from api.helpers.mongo_instance import mongo
from api.models.UsersModels import UserIn, UserOut


async def create_user(user: UserIn) -> Union[UserOut, None]:
    if mongo.db is None:
        raise Exception("MongoDB connection not established.")

    collection = await mongo.get_collection('Users')
    user.password = get_password_hash(user.password)

    try:
        email_check = await collection.find_one({"email": user.email})
        if email_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f" user with email '{user.email}' already exists!"
            )

        handler_check = await collection.find_one({"handler": user.handler})
        if handler_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f" user with handler '{user.handler}' already exists!"
            )

        user = UserOut(**user.dict())

        result = await collection.insert_one(user.to_pymongo())
        if result.acknowledged:
            return user
    except Exception as e:
        raise e
