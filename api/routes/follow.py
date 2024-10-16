from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from api.models.PostModels import Message
from api.services.user import follow_user_service, unfollow_user_service
import logging
import os
import jwt
from dotenv import load_dotenv

load_dotenv()


router = APIRouter(prefix="/users", tags=["followers"])

# Configuração de OAuth2 para recuperar o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração de logging para registrar erros
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


async def get_user_handler_from_token(token: str = Depends(oauth2_scheme)) -> str:
    """Decodifica o token JWT e extrai o user_handler."""
    try:
        # Chave secreta usada para assinar o JWT
        SECRET_KEY = os.getenv("SECRET_KEY")

        # Decodificando o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_handler = payload.get(
            "sub"
        )  # Ajuste conforme o campo que contém o user_handler

        if user_handler is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user_handler not found.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_handler
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/{other_user_handler}/follow", summary="Follow another user")
async def follow_user(
    other_user_handler: str,
    user_handler: str = Depends(get_user_handler_from_token),
) -> Message:
    """Permite que o usuário siga outro usuário."""
    try:
        result = await follow_user_service(user_handler, other_user_handler)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {other_user_handler} not found.",
            )
        return Message(detail="Successfully followed the user.")
    except Exception as e:
        logger.error(f"Failed to follow {other_user_handler}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while following the user.",
        )


@router.put("/{other_user_handler}/unfollow", summary="Unfollow a user")
async def unfollow_user(
    other_user_handler: str,
    user_handler: str = Depends(get_user_handler_from_token),
) -> Message:
    """Permite que o usuário deixe de seguir outro usuário."""
    try:
        result = await unfollow_user_service(user_handler, other_user_handler)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {other_user_handler} not found.",
            )
        return Message(detail="Successfully unfollowed the user.")
    except Exception as e:
        logger.error(f"Failed to unfollow {other_user_handler}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while unfollowing the user.",
        )
