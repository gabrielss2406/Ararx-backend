from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import List, Optional
from api.config.likeException import LikeAlreadyGivenException
from api.dependencies import get_current_user
from api.models.Message import Message
from api.models.PostModels import PostOut, PostUpdateQuery, PostIn
import logging
from api.services.post import (
    create_new_post,
    get_all_posts,
    get_post_by_id,
    update_post_by_id,
    like_post_by_id,
    delete_post_by_id,
    dislike_post_by_id,
    get_posts_by_author,
)
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Define o URL do token

router = APIRouter(
    prefix="/posts",
    tags=["post"],
)

# Configuração básica de logging para registrar erros.
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def not_found_exception(post_id: str) -> HTTPException:
    """Helper para lançar exceção 404 quando um post não é encontrado."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found."
    )


@router.post("/", summary="Create a new post")
def create_post(post: PostIn, token: str = Depends(oauth2_scheme)) -> Message:
    """Cria um novo post, usando o token de autenticação para identificar o usuário."""
    try:
        user = get_current_user(token)
        posted_by = user.handler
        result = create_new_post(posted_by, post.content)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to create post.",
            )
        return Message(message="Post created successfully.")
    except Exception as e:
        logger.error(f"Failed to create post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the post.",
        )


@router.get("/", summary="Get a list of posts")
def get_posts(
    page_num: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0),
    token: str = Depends(oauth2_scheme),
) -> List[PostOut]:
    """Recupera uma lista paginada de posts."""
    try:
        user = get_current_user(token)
        posts = get_all_posts(page_num, page_size, user.handler)
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No posts found."
            )
        return posts
    except Exception as e:
        logger.error(f"Failed to retrieve posts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving posts.",
        )


@router.get("/{post_id}", summary="Get details of a specific post")
def get_post(post_id: str, token: str = Depends(oauth2_scheme)) -> PostOut:
    """Recupera os detalhes de um post específico pelo ID."""
    try:
        user = get_current_user(token)
        post = get_post_by_id(post_id, user.handler)
        if not post:
            raise not_found_exception(post_id)
        return post
    except Exception as e:
        logger.error(f"Failed to retrieve post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the post.",
        )


@router.get("/author/{author}", summary="Get all posts by a specific author")
def get_posts_by_author_route(
    author: str,
    page_num: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0),
    token: str = Depends(oauth2_scheme),
) -> List[PostOut]:
    """Recupera todos os posts de um autor específico."""
    try:
        user = get_current_user(token)
        posts = get_posts_by_author(author, page_num, page_size, user.handler)
        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No posts found for author {author}.",
            )
        return posts
    except Exception as e:
        logger.error(f"Failed to retrieve posts for author {author}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving posts.",
        )


@router.put("/{post_id}", summary="Update a post", response_model=Message)
def update_post(
    post_id: str, query: PostUpdateQuery, token: str = Depends(oauth2_scheme)
) -> Message:
    """Atualiza um post pelo ID."""
    try:
        user = get_current_user(token)
        result = update_post_by_id(post_id, query, user.handler)
        if not result:
            raise not_found_exception(post_id)
        return Message(message="Post updated successfully.")
    except Exception as e:
        logger.error(f"Failed to update post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the post.",
        )


@router.post("/{post_id}/like", summary="Like a post")
def like_post(post_id: str, token: str = Depends(oauth2_scheme)) -> Message:
    """Adiciona um like a um post."""
    try:
        posted_by = get_current_user(token)
        result = like_post_by_id(post_id, posted_by.handler)

        if not result:  # Se o resultado for False, significa que o like já foi dado.
            post = get_post_by_id(post_id)  # Não precisa passar 'posted_by.handler'
            if (
                post and posted_by.handler in post.likes
            ):  # Verifica se o usuário já deu like.
                raise LikeAlreadyGivenException()  # Usando a nova exceção personalizada
            else:  # Se o post não for encontrado.
                raise not_found_exception(post_id)

        return Message(message="Post liked successfully.")
    except LikeAlreadyGivenException as e:
        logger.error(f"Conflict while liking post {post_id}: {str(e)}")
        raise e  # Re-raise the custom exception
    except Exception as e:
        logger.error(f"Failed to like post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while liking the post.",
        )


@router.post("/{post_id}/dislike", summary="Dislike a post")
def dislike_post(post_id: str, token: str = Depends(oauth2_scheme)) -> Message:
    """Remove um like de um post."""
    try:
        posted_by = get_current_user(token)
        result = dislike_post_by_id(post_id, posted_by.handler)
        if not result:
            raise not_found_exception(post_id)
        return Message(message="Post disliked successfully.")
    except Exception as e:
        logger.error(f"Failed to dislike post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while disliking the post.",
        )


@router.delete("/{post_id}", summary="Delete a post")
def delete_post(post_id: str, token: str = Depends(oauth2_scheme)) -> Message:
    """Exclui um post pelo ID."""
    try:
        posted_by = get_current_user(token)
        result = delete_post_by_id(post_id, posted_by.handler)
        if not result:
            raise not_found_exception(post_id)
        return Message(message="Post deleted successfully.")
    except Exception as e:
        logger.error(f"Failed to delete post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the post.",
        )
