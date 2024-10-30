from bson import ObjectId
from starlette import status
from starlette.exceptions import HTTPException
from api.models.CommentModels import CommentOut, CommentIn
from api.services.db import connect_mongo


def create_comment(parent_id: str, comment: CommentIn) -> CommentOut:
    try:
        collection, _ = connect_mongo('Posts')

        comment: CommentOut = CommentOut(**comment.dict())

        result = collection.update_one({"_id": ObjectId(parent_id)},
                                       {"$push": {"comments": comment.to_pymongo()}})

        if result.matched_count == 0:
            result = collection.update_one({"comments._id": ObjectId(parent_id)},
                                           {"$push": {"comments.$.comments": comment.to_pymongo()}})

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent ID {parent_id} was not found")

        return comment
    except Exception as e:
        raise e
