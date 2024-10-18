from api.helpers.mongo_instance import mongo
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import test, register, login, post


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa a conexão com o MongoDB no início
    await mongo.connect()

    if mongo.db is None:
        raise Exception("MongoDB connection not established.")

    print("Connected to MongoDB")

    # Disponibiliza a aplicação
    yield

    # Fecha a conexão com o MongoDB no final
    await mongo.close()
    print("Closed MongoDB connection")


# Passa o gerenciador de ciclo de vida para o FastAPI
app = FastAPI(lifespan=lifespan)

app.include_router(test.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(post.router)


@app.get("/")
def read_root():
    return
