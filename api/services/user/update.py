from typing import Union

from pymongo.errors import DuplicateKeyError
from starlette import status
from starlette.exceptions import HTTPException
from api.models.UsersModels import UserUpdateQuery
from api.services.db import connect_mongo


def update_user(user_handler: str, query: UserUpdateQuery):
    try:

        collection, _ = connect_mongo('Users')
        newValues = {"$set": {}}

        for field in query:
            if field[1] is not None:
                newValues['$set'] = {**newValues['$set'], f'{field[0]}': field[1]}

        result = collection.update_one({"handler": f"{user_handler}"}, newValues)

        if not result:
            return False

        return True

    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'{e.details}'
        )
