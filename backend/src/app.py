from fastapi import FastAPI
from .admin.router import admin_router
from .blog.router import blog_router
from .consoltation.router import consoltation_router
from .meetings.router import meeting_router
from .portfolio.router import portfolio_router
from .users.router import users_router

from starlette.middleware.cors import CORSMiddleware



app = FastAPI()
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(blog_router , prefix="/blog", tags=["blog"])
app.include_router(consoltation_router, prefix="/consoltation", tags=["consoltation"])
app.include_router(meeting_router, prefix="/meeting", tags=["meeting"])
app.include_router(portfolio_router, prefix="/portfolio", tags=["portfolio"])
app.include_router(users_router, prefix="/users", tags=["users"])

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])