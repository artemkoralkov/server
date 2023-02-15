from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates


from modules.lessons.endpoints import lessons_router
from modules.teachers.endpoints import teachers_router

templates = Jinja2Templates(directory='./templates')
app = FastAPI()

origins: 'list[str]' = ['http://localhost:3000',
                      'https://mspu-schedule.netlify.app', 'https://web.postman.co']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lessons_router)
app.include_router(teachers_router)


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
        }
    )
