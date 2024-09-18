from typing import Union

from fastapi import APIRouter

from api.services.db import connect_mongo

router = APIRouter(
    prefix="/test",
    tags=['test']
)


# Testando a conexão com o banco de dados. Deve ser removido posteriormente
@router.get("/")
def read_test() -> Union[list[dict], None]:
    collection, client = connect_mongo('Users')
    result = collection.find({})

    documents: list[dict] = []

    for document in result:
        document["_id"] = str(document["_id"])
        documents.append(document)

    return documents
