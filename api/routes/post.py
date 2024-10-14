from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional, List
from api.models.PostModels import PostOut, PostUpdateQuery, Message, StudentOrderByEnum
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


@router.post("/{post_id}", summary="Create a new post")
async def create_post(post_id: str, posted_by: str) -> Message:
    result = await create_new_post(post_id, posted_by)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Post with id {post_id} already exists!",
        )
    return Message(detail="Post created successfully.")


@router.get("/", summary="Get a list of posts")
async def get_posts(
    page_num: Optional[int] = Query(default=1, gt=0),
    page_size: Optional[int] = Query(default=10, gt=0),
    order_by: Optional[StudentOrderByEnum] = None,
    desc: Optional[bool] = False,
) -> List[PostOut]:
    posts = await get_all_posts(page_num, page_size, order_by, desc)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No posts found."
        )
    return posts


@router.get("/{post_id}", summary="Get details of a specific post")
async def get_post(post_id: str) -> PostOut:
    post = await get_post_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found."
        )
    return post


@router.put("/{post_id}", summary="Update a post")
async def update_post(post_id: str, query: PostUpdateQuery) -> Message:
    result = await update_post_by_id(post_id, query)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found."
        )
    return Message(detail="Post updated successfully.")


@router.put("/{post_id}/like", summary="Like a post")
async def like_post(post_id: str, user_handler: str) -> Message:
    result = await like_post_by_id(post_id, user_handler)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found."
        )
    return Message(detail="Post liked successfully.")


@router.put("/{post_id}/dislike", summary="Dislike a post")
async def dislike_post(post_id: str, user_handler: str) -> Message:
    result = await dislike_post_by_id(post_id, user_handler)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found."
        )
    return Message(detail="Post disliked successfully.")


@router.delete("/{post_id}", summary="Delete a post")
async def delete_post(post_id: str) -> Message:
    result = await delete_post_by_id(post_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found."
        )
    return Message(detail="Post deleted successfully.")
