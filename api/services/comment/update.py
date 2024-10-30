from bson import ObjectId
from pymongo.results import UpdateResult
from starlette import status
from starlette.exceptions import HTTPException

from api.models.CommentModels import CommentUpdateQuery
from api.services.db import connect_mongo


def update_comment(comment_id: str, query: CommentUpdateQuery):
    try:
        collection, _ = connect_mongo("Posts")
        result: UpdateResult

        if query.new_comment is not None:
            result = collection.update_one({"comments._id": ObjectId(comment_id)},
                                           {"$set": {
                                               "comments.$.content": query.new_comment,
                                               "comments.$.edited": True}})

            if result.matched_count == 0:
                post_with_comment = collection.find_one({"comments.comments._id": ObjectId(comment_id)})

                if post_with_comment:
                    for i, comment in enumerate(post_with_comment['comments']):
                        for j, sub_comment in enumerate(comment['comments']):
                            if sub_comment['_id'] == ObjectId(comment_id):
                                result = collection.update_one(
                                    {f"comments.{i}.comments.{j}._id": ObjectId(comment_id)},
                                    {"$set": {
                                        f"comments.{i}.comments.{j}.content": query.new_comment,
                                        f"comments.{i}.comments.{j}.edited": True}})

                                if result.matched_count > 0:
                                    break
                        if result.matched_count > 0:
                            break

            if result.matched_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Comment with id {comment_id} was not found")

        if query.add_or_remove_like is not None:

            post = collection.find_one({"comments._id": ObjectId(comment_id)})
            if not post:
                post = collection.find_one({"comments.comments._id": ObjectId(comment_id)})

            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Comment with id {comment_id} was not found")

            for i, comment in enumerate(post['comments']):
                if comment["_id"] == ObjectId(comment_id):
                    if query.add_or_remove_like in comment["likes"]:
                        result = collection.update_one(
                            {"comments._id": ObjectId(comment_id)},
                            {"$pull": {"comments.$.likes": query.add_or_remove_like}})
                    else:
                        result = collection.update_one(
                            {"comments._id": ObjectId(comment_id)},
                            {"$push": {"comments.$.likes": query.add_or_remove_like}})

                    if result.matched_count > 0:
                        break
                for j, sub_comment in enumerate(comment['comments']):
                    if sub_comment['_id'] == ObjectId(comment_id):
                        if query.add_or_remove_like in sub_comment["likes"]:
                            result = collection.update_one(
                                {f"comments.{i}.comments.{j}._id": ObjectId(comment_id)},
                                {"$pull": {f"comments.{i}.comments.{j}.likes": query.add_or_remove_like}})
                        else:
                            result = collection.update_one(
                                {f"comments.{i}.comments.{j}._id": ObjectId(comment_id)},
                                {"$push": {f"comments.{i}.comments.{j}.likes": query.add_or_remove_like}})

                        if result.matched_count > 0:
                            break
    except Exception as e:
        raise e
