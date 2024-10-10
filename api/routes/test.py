from typing import Union

from fastapi import APIRouter, Security

from api.dependencies import get_current_user
from api.models.UsersModels import UserOut
from api.services.user.read import get_user

router = APIRouter(
    prefix="/test",
    tags=['test'],
    dependencies=[Security(get_current_user)]
)


# Testando a conexão com o banco de dados. Deve ser removido posteriormente
@router.get("/{user_id}")
async def read_test(user_id) -> Union[UserOut, None]:
    user = await get_user(username=user_id)

    return user
