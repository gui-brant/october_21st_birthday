from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.db.indexes import ensure_indexes
from app.db.mongo import close_mongo, connect_mongo
from app.routers import auth, calendar, projects, tasks


@asynccontextmanager
async def lifespan(_app: FastAPI):
    client = await connect_mongo()
    await ensure_indexes(client[settings.mongo_db])
    yield
    await close_mongo()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(calendar.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
