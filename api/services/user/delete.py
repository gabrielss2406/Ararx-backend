from typing import Union
from api.services.db import connect_mongo


def delete_user(user_handler: str) -> Union[True, False]:
    collection, _ = connect_mongo('Users')
    result = collection.delete_one({"handler": f"{user_handler}"})

    if not result.deleted_count:
        return False

    return True
