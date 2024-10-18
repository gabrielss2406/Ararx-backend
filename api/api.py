from api.helpers.mongo_instance import mongo
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import test, register, login, post


# Passa o gerenciador de ciclo de vida para o FastAPI
app = FastAPI()

app.include_router(test.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(post.router)


@app.get("/")
def read_root():
    return
