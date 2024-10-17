from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Optional

from api.models.Message import Message
from api.models.PostModels import PostOut, PostUpdateQuery, PostOrderByEnum
import logging
from api.services.post import (
    create_new_post,
    get_all_posts,
    get_post_by_id,
    update_post_by_id,
    like_post_by_id,
    dislike_post_by_id,
    delete_post_by_id,
)

router = APIRouter(prefix="/posts", tags=["posts"])

# Configuração básica de logging para registrar erros.
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def not_found_exception(post_id: str) -> HTTPException:
    """Helper para lançar exceção 404 quando um post não é encontrado."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found."
    )


@router.post("/", summary="Create a new post")
async def create_post(post_id: str, posted_by: str) -> Message:
    """Cria um novo post com um ID único."""
    try:
        result = await create_new_post(post_id, posted_by)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Post with id {post_id} already exists!",
            )
        return Message(detail="Post created successfully.")
    except Exception as e:
        logger.error(f"Failed to create post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the post.",
        )


@router.get("/", summary="Get a list of posts")
async def get_posts(
    page_num: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0),
    order_by: Optional[PostOrderByEnum] = None,
    desc: bool = False,
) -> List[PostOut]:
    """Recupera uma lista paginada de posts."""
    try:
        posts = await get_all_posts(page_num, page_size, order_by, desc)
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
async def get_post(post_id: str) -> PostOut:
    """Recupera os detalhes de um post específico pelo ID."""
    try:
        post = await get_post_by_id(post_id)
        if not post:
            raise not_found_exception(post_id)
        return post
    except Exception as e:
        logger.error(f"Failed to retrieve post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the post.",
        )


@router.put("/{post_id}", summary="Update a post")
async def update_post(post_id: str, query: PostUpdateQuery) -> Message:
    """Atualiza um post pelo ID."""
    try:
        result = await update_post_by_id(post_id, query)
        if not result:
            raise not_found_exception(post_id)
        return Message(detail="Post updated successfully.")
    except Exception as e:
        logger.error(f"Failed to update post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the post.",
        )


@router.post("/{post_id}/like", summary="Like a post")
async def like_post(post_id: str, user_handler: str) -> Message:
    """Adiciona um like a um post."""
    try:
        result = await like_post_by_id(post_id, user_handler)
        if not result:
            raise not_found_exception(post_id)
        return Message(detail="Post liked successfully.")
    except Exception as e:
        logger.error(f"Failed to like post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while liking the post.",
        )


@router.post("/{post_id}/dislike", summary="Dislike a post")
async def dislike_post(post_id: str, user_handler: str) -> Message:
    """Adiciona um dislike a um post."""
    try:
        result = await dislike_post_by_id(post_id, user_handler)
        if not result:
            raise not_found_exception(post_id)
        return Message(detail="Post disliked successfully.")
    except Exception as e:
        logger.error(f"Failed to dislike post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while disliking the post.",
        )


@router.delete("/{post_id}", summary="Delete a post")
async def delete_post(post_id: str) -> Message:
    """Exclui um post pelo ID."""
    try:
        result = await delete_post_by_id(post_id)
        if not result:
            raise not_found_exception(post_id)
        return Message(detail="Post deleted successfully.")
    except Exception as e:
        logger.error(f"Failed to delete post {post_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the post.",
        )
