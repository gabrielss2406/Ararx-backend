from typing import Union

from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.exceptions import HTTPException
from api.dependencies import get_password_hash
from api.helpers.mongo_instance import mongo
from api.models.UsersModels import UserIn, UserOut
from api.services.db import connect_mongo


def create_user(user: UserIn) -> Union[UserOut, None]:
    if mongo.db is None:
        raise Exception("MongoDB connection not established.")

    collection, _ = connect_mongo('Users')
    user.password = get_password_hash(user.password)

    try:
        user = UserOut(**user.dict())

        result = collection.insert_one(user.to_pymongo())
        if result.acknowledged:
            return user

    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{e.details}'
        )
    except Exception as e:
        raise e
