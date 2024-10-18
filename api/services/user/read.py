from typing import Union

from api.helpers.mongo_instance import mongo
from api.helpers.verifyEmail import is_email
from api.models.UsersModels import UserOut
from api.services.db import connect_mongo


def get_user(username: str) -> Union[UserOut, None]:
    if is_email(username):
        user_key = "email"
    else:
        user_key = "handler"

    collection, _ = connect_mongo('Users')
    result = collection.find_one({f"{user_key}": f"{username}"})

    if not result:
        return None

    return UserOut(**result)
