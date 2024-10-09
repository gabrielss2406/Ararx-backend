from typing import Union
from connection.database import MongoDB
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.services.db import connect_mongo
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()


MONGO_URI = os.getenv("MONGO_URI")

mongo = MongoDB(MONGO_URI, "ararx")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa a conexão com o MongoDB no início
    await mongo.connect()
    print("Connected to MongoDB")

    # Disponibiliza a aplicação
    yield

    # Fecha a conexão com o MongoDB no final
    await mongo.close()
    print("Closed MongoDB connection")

# Passa o gerenciador de ciclo de vida para o FastAPI
app = FastAPI(lifespan=lifespan)

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
