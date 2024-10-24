from api.models.CommentModels import CommentUpdateQuery
from api.services.db import connect_mongo


def update_comment(query: CommentUpdateQuery):
    try:
        collection, _ = connect_mongo("Posts")
        result = collection.update_one()
    except Exception as e:
        raise e