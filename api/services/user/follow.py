from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException, status
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("ararx")


# Função para seguir um usuário
async def follow_user_service(current_user: str, other_user: str) -> Optional[bool]:
    if current_user == other_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode seguir a si mesmo.",
        )

    # Verifica se o outro usuário existe
    user = await db.users.find_one({"user_handler": other_user})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )

    # Adiciona o usuário à lista de seguidores se ainda não foi seguido
    result = await db.users.update_one(
        {"user_handler": current_user}, {"$addToSet": {"following": other_user}}
    )
    return result.modified_count > 0


# Função para deixar de seguir um usuário
async def unfollow_user_service(current_user: str, other_user: str) -> Optional[bool]:
    if current_user == other_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode deixar de seguir a si mesmo.",
        )

    # Verifica se o outro usuário existe
    user = await db.users.find_one({"user_handler": other_user})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )

    # Remove o usuário da lista de seguidores se ele estiver na lista
    result = await db.users.update_one(
        {"user_handler": current_user}, {"$pull": {"following": other_user}}
    )
    return result.modified_count > 0
