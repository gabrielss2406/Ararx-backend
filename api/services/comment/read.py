from bson import ObjectId
from pymongo import DESCENDING
from api.models.CommentModels import CommentQueryParams, CommentOut
from api.services.db import connect_mongo
from typing import List


def sort_comments_recursively(
    comments: List[dict], order_by: str, desc: bool
) -> List[dict]:
    # Ordena os comentários do nível atual
    sorted_comments = sorted(
        comments,
        key=lambda x: x.get(order_by, None),  # Garantir que a chave existe
        reverse=desc,
    )
    # Ordena recursivamente os subcomentários
    for comment in sorted_comments:
        if comment.get("comments"):
            comment["comments"] = sort_comments_recursively(
                comment["comments"], order_by, desc
            )
    return sorted_comments


def get_comments(post_id: str, params: CommentQueryParams) -> List[CommentOut]:
    try:
        collection, _ = connect_mongo("Posts")

        # Recupera o post com seus comentários
        result = collection.find_one({"_id": ObjectId(post_id)})

        if not result or "comments" not in result or not result["comments"]:
            return []

        # Ordena os comentários principais
        sorted_comments = sorted(
            result["comments"],
            key=lambda x: x.get(
                params.order_by.value, None
            ),  # Ordena pela chave indicada
            reverse=params.desc,
        )

        # Ordena recursivamente os subcomentários
        sorted_comments = sort_comments_recursively(
            sorted_comments, params.order_by.value, params.desc
        )

        # Aplica a paginação
        start = (params.page_num - 1) * params.page_size
        end = start + params.page_size
        paginated_comments = sorted_comments[start:end]

        # Converte os resultados para CommentOut
        comments = [CommentOut(**comment) for comment in paginated_comments]
        return comments

    except Exception as e:
        raise e
