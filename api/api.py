from typing import Union
from connection.database import MongoDB
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.services.db import connect_mongo
from dotenv import load_dotenv
import os

from fastapi import FastAPI

from api.routes import test, register, login

load_dotenv()
app = FastAPI()

app.include_router(test.router)
app.include_router(register.router)
app.include_router(login.router)


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
