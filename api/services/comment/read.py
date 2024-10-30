from bson import ObjectId

from api.models.CommentModels import CommentQueryParams, CommentOut
from api.services.db import connect_mongo


def get_comments(post_id: str, params: CommentQueryParams) -> list[CommentOut]:
    try:
        collection, _ = connect_mongo("Posts")
        result = collection.find_one({"_id": ObjectId(post_id)})
        print(result)
        if len(result["comments"]) <= 0:
            return []

        sorted_result = sorted(result["comments"], key=lambda x: x[params.order_by.value], reverse=params.desc)

        start = (params.page_num - 1) * params.page_size
        end = start + params.page_size

        comments: list[CommentOut] = []
        for comment in sorted_result[start:end]:
            comments.append(CommentOut(**comment))

        return comments

    except Exception as e:
        raise e