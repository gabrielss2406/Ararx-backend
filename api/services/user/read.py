from typing import Union

from api.helpers.mongo_instance import mongo
from api.helpers.verifyEmail import is_email
from api.models.UsersModels import UserOut


async def get_user(username: str) -> Union[UserOut, None]:
    if is_email(username):
        user_key = "email"
    else:
        user_key = "handler"

    collection = await mongo.get_collection('Users')
    result = await collection.find_one({f"{user_key}": f"{username}"})

    if not result:
        return None

    return UserOut(**result)
