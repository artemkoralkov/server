from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from src.database import Base, engine
from src.lessons.router import lessons_router
from src.rooms.router import rooms_router
from src.teachers.router import teachers_router
from src.users.router import users_router
from src.logs.router import logs_router

templates = Jinja2Templates(directory="./templates")
app = FastAPI()


origins: "list[str]" = [
    "http://localhost:3000",
    "http://192.168.0.103:3000",
    "http://192.168.0.103:3000/",
    "https://mspu-schedule.netlify.app",
    "https://web.postman.co",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(engine, checkfirst=True)

app.include_router(lessons_router)
app.include_router(teachers_router)
app.include_router(rooms_router)
app.include_router(users_router)
app.include_router(logs_router)
