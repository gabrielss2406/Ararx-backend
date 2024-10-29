from typing import Optional, List
from api.models.PostModels import PostOut, PostUpdateQuery
from datetime import datetime
from api.services.db.mongo_connection import connect_mongo
from bson import ObjectId


def create_new_post(posted_by: str, content: str) -> bool:
    """Cria uma nova postagem com um ID gerado automaticamente. Retorna True se a postagem foi criada com sucesso, False se já existe."""
    collection, _ = connect_mongo("Posts")
    post_id = ObjectId()  # Gerar um novo ObjectId automaticamente

    post_data = {
        "_id": post_id,
        "author": posted_by,  # Certifique-se de que 'posted_by' é uma string
        "content": content,
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
    cursor = (
        collection.find().sort("date", -1).skip(skip).limit(page_size)
    )  # Ordena do mais novo para o mais velho

    posts = cursor.to_list(length=page_size)
    return [PostOut(**post) for post in posts]


def get_post_by_id(post_id: str) -> Optional[PostOut]:
    """Recupera uma postagem específica pelo ID. Retorna PostOut ou None se não encontrado."""
    collection, _ = connect_mongo("Posts")
    post = collection.find_one({"_id": ObjectId(post_id)})
    if post:
        return PostOut(**post)
    return None


def get_posts_by_author(
    author: str, page_num: int = 1, page_size: int = 10
) -> List[PostOut]:
    """Recupera todos os posts de um autor específico com paginação. Retorna uma lista de PostOut."""
    collection, _ = connect_mongo("Posts")
    skip = (page_num - 1) * page_size
    cursor = (
        collection.find({"author": author}).sort("date", -1).skip(skip).limit(page_size)
    )  # Ordena do mais novo para o mais velho

    posts = cursor.to_list(length=page_size)
    return [PostOut(**post) for post in posts]


def update_post_by_id(post_id: str, query: PostUpdateQuery, user: str) -> bool:
    """Atualiza uma postagem específica. Retorna True se a postagem foi atualizada, False se não encontrada ou se o usuário não é o autor."""
    collection, _ = connect_mongo("Posts")
    post = collection.find_one({"_id": ObjectId(post_id)})
    if post and post["author"] == user:  # Verifica se o usuário é o autor do post
        result = collection.update_one(
            {"_id": ObjectId(post_id)}, {"$set": query.dict(exclude_unset=True)}
        )
        return result.modified_count > 0
    return False


def like_post_by_id(post_id: str, user: str) -> bool:
    """Adiciona um like à postagem. Retorna True se o like foi adicionado, False se não encontrada."""
    collection, _ = connect_mongo("Posts")
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {
            "$addToSet": {"likes": user},  # Usa $addToSet para evitar duplicatas
            "$set": {"date": datetime.now()},
        },
    )
    return result.modified_count > 0


def dislike_post_by_id(post_id: str, user: str) -> bool:
    """Remove um like da postagem. Retorna True se o dislike foi aplicado, False se não encontrada."""
    collection, _ = connect_mongo("Posts")
    result = collection.update_one(
        {"_id": ObjectId(post_id)},
        {
            "$pull": {"likes": user},  # Usa $pull para remover o like
            "$set": {"date": datetime.now()},
        },
    )
    return result.modified_count > 0


def delete_post_by_id(post_id: str, user: str) -> bool:
    """Exclui uma postagem pelo ID. Retorna True se a postagem foi excluída, False se não encontrada ou se o usuário não é o autor."""
    collection, _ = connect_mongo("Posts")
    post = collection.find_one({"_id": ObjectId(post_id)})
    if post and post["author"] == user:  # Verifica se o usuário é o autor do post
        result = collection.delete_one({"_id": ObjectId(post_id)})
        return result.deleted_count > 0
    return False
