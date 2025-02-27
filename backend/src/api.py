from datetime import time
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import time
from routers.admin import admin_router
from routers.auth import auth_router
from routers.article import articles_router
from routers.comment import comments_router
from routers.consolation import consoltation_router
from routers.meeting import meeting_router
from routers.portfolio import portfolio_router
from routers.users import users_router
from routers.files import file_router
from routers.tasks import tasks_router

from db.database import get_db
from models.role import create_default_roles
from models.user import create_admin_users
from db.database import create_all_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


# Example startup and shutdown logic
async def startup():
    print("Starting up...")
    await create_all_tables()  # Create tables asynchronously
    async for db in get_db():  # Get the async session
        await create_default_roles(db)  # Create default roles asynchronously
        await create_admin_users(db)
    print("App Started...")

async def shutdown():
    print("Shutting down...")
    # Perform cleanup tasks (e.g., close database connections)


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


import os

# Get the absolute path of the current script
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

app.mount("/statics/files", StaticFiles(directory=f"{current_directory}/statics/files"), name="files")





@app.middleware("http")
async def add_durations(request: Request, call_next):
    start_time  = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response