from fastapi import FastAPI

from api.services.db import connect_mongo

app = FastAPI()


@app.get("/")
def read_root():
    return


# Testando a conexão com o banco de dados. Deve ser removido posteriormente
@app.get("/test")
def read_test():
    collection, client = connect_mongo('Users')
    result = collection.find({})

    for document in result:
        print(document)

    return None
