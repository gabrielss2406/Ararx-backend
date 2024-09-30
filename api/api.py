from fastapi import FastAPI

from api.routes import test, register, login

app = FastAPI()

app.include_router(test.router)
app.include_router(register.router)
app.include_router(login.router)


@app.get("/")
def read_root():
    return
