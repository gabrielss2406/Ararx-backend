from fastapi import HTTPException, status
from typing import Optional
from dotenv import load_dotenv
from api.services.db import connect_mongo
import os

# Função para seguir um usuário
async def follow_user_service(current_user: str, other_user: str) -> Optional[bool]:
    if current_user == other_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode seguir a si mesmo.",
        )
    user_key = "handler"

    # Verifica se o outro usuário existe
    collection, _ = connect_mongo("Users")
    user = collection.find_one({f"{user_key}": f"{other_user}"})
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )

    # Adiciona o usuário à lista de seguidores se ainda não foi seguido
    result = collection.update_one(
        {"handler": current_user}, {"$addToSet": {"following": other_user}}
    )
    return result.modified_count > 0


# Função para deixar de seguir um usuário
async def unfollow_user_service(current_user: str, other_user: str) -> Optional[bool]:
    if current_user == other_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode deixar de seguir a si mesmo.",
        )

    user_key = "handler"

    # Verifica se o outro usuário existe
    collection, _ = connect_mongo("Users")
    user = collection.find_one({f"{user_key}": f"{other_user}"})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )

    # Remove o usuário da lista de seguidores se ele estiver na lista
    result = collection.update_one(
        {"handler": current_user}, {"$pull": {"following": other_user}}
    )
    return result.modified_count > 0
