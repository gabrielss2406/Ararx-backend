from typing import Optional, List
from api.models.PostModels import PostOut, PostUpdateQuery
from datetime import datetime
from dotenv import load_dotenv
import os
from api.connection.database import MongoDB

from api.helpers.mongo_instance import mongo
from api.models.PostModels import PostOut, PostUpdateQuery
from datetime import datetime


def create_new_post(post_id: str, posted_by: str) -> bool:
    """Cria uma nova postagem."""
    posts_collection = mongo.get_collection("Posts")
    existing_post = posts_collection.find_one({"_id": post_id})
    if existing_post:
        return False  # Postagem já existe

    post_data = {
        "_id": post_id,
        "posted_by": posted_by,
        "likes": 0,
        "dislikes": 0,
        "created_at": datetime.now(datetime.timezone.utc),
        "updated_at": datetime.now(datetime.timezone.utc),
    }
    posts_collection.insert_one(post_data)
    return True


def get_all_posts(
    page_num: int, page_size: int, order_by: Optional[str] = None, desc: bool = False
) -> List[PostOut]:
    """Recupera uma lista de postagens com paginação e ordenação."""
    posts_collection = mongo.get_collection("Posts")
    skip = (page_num - 1) * page_size
    order = -1 if desc else 1
    cursor = posts_collection.find().skip(skip).limit(page_size)

    if order_by:
        cursor = cursor.sort(order_by, order)

    posts = cursor.to_list(length=page_size)
    return [PostOut(**post) for post in posts]


def get_post_by_id(post_id: str) -> Optional[PostOut]:
    """Recupera uma postagem específica pelo ID."""
    posts_collection = mongo.get_collection("Posts")
    post = posts_collection.find_one({"_id": post_id})
    if post:
        return PostOut(**post)
    return None


def update_post_by_id(post_id: str, query: PostUpdateQuery) -> bool:
    """Atualiza uma postagem específica."""
    posts_collection = mongo.get_collection("Posts")
    result = posts_collection.update_one(
        {"_id": post_id}, {"$set": query.dict(exclude_unset=True)}
    )
    return result.modified_count > 0


def like_post_by_id(post_id: str, user_handler: str) -> bool:
    """Adiciona um like à postagem."""
    posts_collection = mongo.get_collection("Posts")
    result = posts_collection.update_one(
        {"_id": post_id},
        {"$inc": {"likes": 1}, "$set": {"updated_at": datetime.utcnow()}},
    )
    return result.modified_count > 0


def dislike_post_by_id(post_id: str, user_handler: str) -> bool:
    """Adiciona um dislike à postagem."""
    posts_collection = mongo.get_collection("Posts")
    result = posts_collection.update_one(
        {"_id": post_id},
        {"$inc": {"dislikes": 1}, "$set": {"updated_at": datetime.utcnow()}},
    )
    return result.modified_count > 0


def delete_post_by_id(post_id: str) -> bool:
    """Exclui uma postagem pelo ID."""
    posts_collection = mongo.get_collection("Posts")
    result = posts_collection.delete_one({"_id": post_id})
    return result.deleted_count > 0
