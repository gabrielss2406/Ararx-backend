from typing import Optional

from fastapi import APIRouter

from api.models.CommentModels import CommentOut, CommentUpdateQuery, CommentIn, CommentParentTypeEnum
from api.models.Message import Message
from api.services.comment.create import create_comment as create_comment_by_id


router = APIRouter(
    prefix='/comments',
    tags=['comments']
)


@router.post("/create_comment/{parent_id}")
def create_comment(parent_id: str, comment: CommentIn) -> Message:
    try:
        new_comment: CommentOut = create_comment_by_id(parent_id=parent_id, comment=comment)

        if new_comment:
            return Message(message=f'comment with id {new_comment.id} created successfully',
                           details={'new_comment': new_comment})
    except Exception as e:
        raise e

# @router.get("/comments")
# def get_comments(
# page_num: Optional[int] = Query(default=None, gt=0),
# page_size: Optional[int] = Query(default=None, gt=0),
# order_by: Optional[StudentOrderByEnum] = None,
# desc: Optional[bool] = None
# ) -> list[CommentOut]:
# pass
#
# @router.get("/{post_id}")
# def get_comments_by_post(post_id: str) -> list(CommentOut):
#     try:
#         result = get_comments_by_post
#     except Exception as e:
#         raise e


# @router.put("/{comment_id}")
# def edit_comment(comment_id: str, new_comment: str) -> Message:
#     try:
#         result = edit_comment_by_id(comment_id=comment_id, new_comment=new_comment)
#
#         return result
#     except Exception as e:
#         raise e

# @router.put("/{comment_id}")
# def like_comment(comment_id: str, user_handler: str) -> Message:
# pass
#
# @router.put("/{comment_id}")
# def dislike_comment(comment_id: str, user_handler: str) -> Message:
# pass
#
# @router.delete("/{comment_id}")
# def delete_comment(comment_id: str) -> Message:
# pass
