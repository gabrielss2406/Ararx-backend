from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException

from api.dependencies import get_current_user
from api.models.Message import Message
from api.models.UsersModels import UserOut, UserUpdateQuery, UserQueryParams
from api.services.user.read import get_user as get_user_by_handler, get_multiple_users
from api.services.user.update import update_user as update_user_by_handler
from api.services.user.delete import delete_user as delete_user_by_handler

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get("/")
def get_users(params: UserQueryParams = Depends()) -> list[UserOut]:
    try:
        print(params)
        result = get_multiple_users(params)

        return result
    except Exception as e:
        raise e


@router.get("/{user_handler}")
def get_user(user_handler: str, current_user: Annotated[UserOut, Depends(get_current_user)]) -> UserOut:
    try:
        result = get_user_by_handler(user_handler)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'user with handler {user_handler} was not found'
            )

        if result.id in current_user.followers:
            result.isFollowing = True

        if result.id == current_user.id:
            result.isMe = True

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
