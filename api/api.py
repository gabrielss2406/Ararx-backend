from api.dependencies import get_api_key
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Security
from api.routes import test, register, login, post, comments, user, follow

app = FastAPI(
    dependencies=[Security(get_api_key)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router)
app.include_router(login.router)
app.include_router(post.router)
app.include_router(comments.router)
app.include_router(user.router)
app.include_router(follow.router)

@app.get("/")
def read_root():
    return
