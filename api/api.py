from typing import Union

from fastapi import FastAPI

from api.services.db import connect_mongo

app = FastAPI()


@app.get("/")
def read_root():
    return


# Testando a conexão com o banco de dados. Deve ser removido posteriormente
@app.get("/test")
def read_test() -> Union[list[dict], None]:
    collection, client = connect_mongo('Users')
    result = collection.find({})

    documents: list[dict] = []

    for document in result:
        document["_id"] = str(document["_id"])
        documents.append(document)

    return documents
