from fastapi import APIRouter, HTTPException, Depends, status, Security
from api.services.user.follow import follow_user_service, unfollow_user_service
from dotenv import load_dotenv
from api.dependencies import get_current_user, get_api_key

load_dotenv()

router = APIRouter(
    prefix="/follow",
    tags=["follow"],
    dependencies=[Depends(get_api_key)],
)


@router.put("/users/{other_user_handler}")
async def follow_user(
    other_user_handler: str,
    current_user: dict = Security(get_current_user),
) -> dict:
    user_handler = current_user.handler
    result = await follow_user_service(user_handler, other_user_handler)
    print(result)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível seguir o usuário.",
        )

    return {"detail": "Usuário seguido com sucesso."}


@router.put("/users/{other_user_handler}/unfollow")
async def unfollow_user(
    other_user_handler: str,
    current_user: dict = Security(get_current_user),
) -> dict:
    user_handler = current_user.handler
    result = await unfollow_user_service(user_handler, other_user_handler)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível deixar de seguir o usuário.",
        )

    return {"detail": "Deixou de seguir o usuário com sucesso."}
