from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException

from api.dependencies import get_current_user
from api.models.CommentModels import CommentOut, CommentUpdateQuery, CommentIn, CommentParentTypeEnum, \
    CommentQueryParams
from api.models.Message import Message
from api.models.UsersModels import UserOut
from api.services.comment.create import create_comment as create_comment_by_id
from api.services.comment.read import get_comments as get_comments_by_query
from api.services.comment.update import update_comment as edit_comment_by_id
from api.services.comment.delete import delete_comment as delete_comment_by_id

router = APIRouter(
    prefix='/comments',
    tags=['comments']
)


@router.post("/create/{parent_id}", description="Creates a new comment on a post")
def create_comment(
        parent_id: str,
        comment: CommentIn,
        current_user: Annotated[UserOut, Depends(get_current_user)]
) -> Message:
    try:
        new_comment: CommentOut = create_comment_by_id(parent_id=parent_id, comment=comment, current_user=current_user)

        if new_comment:
            return Message(message=f'comment with id {new_comment.id} created successfully',
                           details={'new_comment': new_comment})
    except Exception as e:
        raise e


@router.get("/{post_id}", description="Returns the comments of a post")
def get_comments(post_id: str, query: CommentQueryParams = Depends()) -> list[CommentOut]:
    try:
        result = get_comments_by_query(post_id, query)
        return result
    except Exception as e:
        raise e


@router.put("/edit/{comment_id}")
def edit_comment(comment_id: str, new_comment: str) -> Message:
    try:
        result = edit_comment_by_id(comment_id=comment_id, query=CommentUpdateQuery(new_comment=new_comment))

        return Message(message=f"comment with id {comment_id} updated successfully")
    except Exception as e:
        raise e


@router.put("/like/{comment_id}")
def like_comment(
        comment_id: str,
        current_user: Annotated[UserOut, Depends(get_current_user)]
) -> Message:
    try:
        result = edit_comment_by_id(
            comment_id=comment_id,
            query=CommentUpdateQuery(add_or_remove_like=current_user.handler))

        return Message(message=f"comment with id {comment_id} liked by {current_user.handler} successfully")
    except Exception as e:
        raise e


@router.put("/dislike/{comment_id}")
def dislike_comment(
        comment_id: str,
        current_user: Annotated[UserOut, Depends(get_current_user)]
) -> Message:
    try:
        result = edit_comment_by_id(
            comment_id=comment_id,
            query=CommentUpdateQuery(add_or_remove_like=current_user.handler))

        return Message(message=f"comment with id {comment_id} diliked by {current_user.handler} successfully")
    except Exception as e:
        raise e


@router.delete("/delete/{comment_id}")
def delete_comment(comment_id: str) -> Message:
    try:
        result = delete_comment_by_id(comment_id=comment_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"comment with id {comment_id} was not found"
            )

        return Message(message=f"comment with id {comment_id} was deleted successfully")

    except Exception as e:
        raise e
