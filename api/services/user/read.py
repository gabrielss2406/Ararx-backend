from typing import Union
from api.helpers.verifyEmail import is_email
from api.models.UsersModels import UserOut, UserQueryParams
from api.services.db import connect_mongo


def get_user(username: str) -> Union[UserOut, None]:
    try:
        if is_email(username):
            user_key = "email"
        else:
            user_key = "handler"

        collection, _ = connect_mongo('Users')
        result = collection.find_one({f"{user_key}": f"{username}"})

        if not result:
            return None

        return UserOut(**result)
    except Exception as e:
        raise e


def get_multiple_users(params: UserQueryParams) -> list[UserOut]:
    try:
        collection, _ = connect_mongo('Users')
        sort = [(f"{params.order_by.value}", 1 if not params.desc else -1)]
        skip = (params.page_num - 1) * params.page_size

        result = collection.find().sort(sort).skip(skip).limit(params.page_size)
        users: list[UserOut] = []

        for user in result:
            users.append(UserOut(**user))

        return users
    except Exception as e:
        raise e