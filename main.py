from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from middleware import todo_middleware
from logger import logger
from database import engine
import models
from routers import auth, todo, user
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(user.router)


app.mount("/static", StaticFiles(directory="static"), name="static")



logger.info("starting app")
app.add_middleware(BaseHTTPMiddleware, dispatch=todo_middleware)

models.Base.metadata.create_all(bind=engine)

@app.get('/')
async def home():
    return {'message': 'Hello Home!'}










