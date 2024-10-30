from bson import ObjectId
from bson.errors import InvalidId
from starlette import status
from starlette.exceptions import HTTPException
from api.services.db import connect_mongo


def delete_comment(comment_id: str) -> bool:
    try:
        collection, _ = connect_mongo('Posts')

        result = collection.update_one(
            {"comments._id": ObjectId(comment_id)},
            {"$pull": {"comments": {"_id": ObjectId(comment_id)}}}
        )

        if result.modified_count > 0:
            return True

        result = collection.update_one(
            {"comments.comments._id": ObjectId(comment_id)},
            {"$pull": {"comments.$[].comments": {"_id": ObjectId(comment_id)}}}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with id {comment_id} not found"
            )

        return True

    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"id {comment_id} is not a valid ObjectId"
        )

    except Exception as e:
        raise e
