from datetime import time
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import time

from .admin import admin_router
from .auth import auth_router
from .article import articles_router
from .comment import comments_router
from .consolation import consoltation_router
from .meeting import meeting_router
from .portfolio import portfolio_router
from .users import users_router
from .files import file_router
from .tasks import tasks_router


# Example startup and shutdown logic
async def startup():
    print("Starting up...")
    # Perform startup tasks (e.g., connect to database)

async def shutdown():
    print("Shutting down...")
    # Perform cleanup tasks (e.g., close database connections)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(articles_router , prefix="/article", tags=["article"])
app.include_router(comments_router , prefix="/comment", tags=["comment"])
app.include_router(consoltation_router, prefix="/consoltation", tags=["consoltation"])
app.include_router(meeting_router, prefix="/meeting", tags=["meeting"])
app.include_router(portfolio_router, prefix="/portfolio", tags=["portfolio"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(file_router,prefix="/static",tags=["file"])
app.include_router(tasks_router,prefix="/tasks",tags=["tssks"])



app.add_middleware(CORSMiddleware,
                    allow_origins=["*"],
                    allow_methods=["*"],
                    allow_headers=["*"],
                    allow_credentials= True,
                    allow_origin_regex= None,
                    expose_headers= (),
                    max_age= 600
                )


app.mount("/files", StaticFiles(directory="/Users/sina/Documents/github/portfolio/backend/files"), name="files")





@app.middleware("http")
async def add_durations(request: Request, call_next):
    start_time  = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response