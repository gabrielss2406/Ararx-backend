from typing import Optional, List
from api.models.PostModels import PostOut, PostUpdateQuery
from datetime import datetime
from api.services.db.mongo_connection import connect_mongo
from bson import ObjectId


def create_new_post(posted_by: str) -> bool:
    """Cria uma nova postagem com um ID gerado automaticamente. Retorna True se a postagem foi criada com sucesso, False se já existe."""
    collection, _ = connect_mongo("Posts")
    post_id = ObjectId()  # Gerar um novo ObjectId automaticamente
    existing_post = collection.find_one({"_id": post_id})

    post_data = {
        "_id": post_id,  # Use o novo ObjectId gerado
        "author": posted_by,
        "content": "testando: " + str(post_id),
        "date": str(datetime.now()),
        "likes": [],
        "reposts": [],
        "comments": [],
    }
    collection.insert_one(post_data)
    return True


def get_all_posts(page_num: int = 1, page_size: int = 10) -> List[PostOut]:
    """Recupera uma lista de postagens com paginação. Retorna uma lista de PostOut."""
    collection, _ = connect_mongo("Posts")
    skip = (page_num - 1) * page_size
    cursor = collection.find().skip(skip).limit(page_size)

    posts = cursor.to_list(length=page_size)
    return [PostOut(**post) for post in posts]


def get_post_by_id(post_id: str) -> Optional[PostOut]:
    """Recupera uma postagem específica pelo ID. Retorna PostOut ou None se não encontrado."""
    collection, _ = connect_mongo("Posts")
    post = collection.find_one({"_id": ObjectId(post_id)})  # Use ObjectId
    if post:
        return PostOut(**post)
    return None


def get_posts_by_author(
    author: str, page_num: int = 1, page_size: int = 10
) -> List[PostOut]:
    """Recupera todos os posts de um autor específico com paginação. Retorna uma lista de PostOut."""
    collection, _ = connect_mongo("Posts")
    skip = (page_num - 1) * page_size
    cursor = collection.find({"author": author}).skip(skip).limit(page_size)

    posts = cursor.to_list(length=page_size)
    return [PostOut(**post) for post in posts]


def update_post_by_id(post_id: str, query: PostUpdateQuery) -> bool:
    """Atualiza uma postagem específica. Retorna True se a postagem foi atualizada, False se não encontrada."""
    collection, _ = connect_mongo("Posts")
    result = collection.update_one(
        {"_id": ObjectId(post_id)}, {"$set": query.dict(exclude_unset=True)}
    )
    return result.modified_count > 0


def like_post_by_id(post_id: str, handler: str) -> bool:
    """Adiciona um like à postagem. Retorna True se o like foi adicionado, False se não encontrada."""
    collection, _ = connect_mongo("Posts")
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {
            "$addToSet": {"likes": handler},  # Usa $addToSet para evitar duplicatas
            "$set": {"date": datetime.now()},
        },
    )
    return result.modified_count > 0


def dislike_post_by_id(post_id: str, handler: str) -> bool:
    """Remove um like da postagem. Retorna True se o dislike foi aplicado, False se não encontrada."""
    collection, _ = connect_mongo("Posts")
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {
            "$pull": {"likes": handler},  # Usa $pull para remover o like
            "$set": {"date": datetime.now()},
        },
    )
    return result.modified_count > 0


def delete_post_by_id(post_id: str) -> bool:
    """Exclui uma postagem pelo ID. Retorna True se a postagem foi excluída, False se não encontrada."""
    collection, _ = connect_mongo("Posts")
    result = collection.delete_one({"_id": ObjectId(post_id)})
    return result.deleted_count > 0
