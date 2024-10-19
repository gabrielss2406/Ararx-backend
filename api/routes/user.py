from typing import Optional

from fastapi import APIRouter, Query
from starlette import status
from starlette.exceptions import HTTPException

from api.models.Message import Message
from api.models.UsersModels import UserOut, UserUpdateQuery
from api.services.user.read import get_user as get_user_by_handler
from api.services.user.update import update_user as update_user_by_handler
from api.services.user.delete import delete_user as delete_user_by_handler

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# @router.get("/")
# def get_users(
# page_num: Optional[int] = Query(default=None, gt=0),
# page_size: Optional[int] = Query(default=None, gt=0),
# order_by: Optional[UserOrderByEnum] = None,
# desc: Optional[bool] = None
# ) -> list[UserOut]:
# pass

@router.get("/{user_handler}")
def get_user(user_handler: str) -> UserOut:
    try:
        result = get_user_by_handler(user_handler)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'user with handler {user_handler} was not found'
            )
        return result
    except Exception as e:
        raise e


@router.put("/{user_handler}")
def update_user(user_handler: str, query: UserUpdateQuery) -> Message:
    try:
        result = update_user_by_handler(user_handler, query)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'user with handler {user_handler} was not found'
            )

        return Message(message=f'user with handler {user_handler} was updated')
    except Exception as e:
        raise e


@router.delete("/{user_handler}")
def delete_user(user_handler: str) -> Message:
    try:
        result = delete_user_by_handler(user_handler)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'user with handler {user_handler} was not found'
            )
        return Message(message=f'user with handler {user_handler} was deleted')
    except Exception as e:
        raise e
