from collections.abc import AsyncIterator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.settings import settings

client: AsyncIOMotorClient | None = None


async def connect_mongo() -> AsyncIOMotorClient:
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.mongo_uri)
    return client


async def close_mongo() -> None:
    global client
    if client is not None:
        client.close()
        client = None


async def get_db() -> AsyncIterator[AsyncIOMotorDatabase]:
    mongo_client = await connect_mongo()
    yield mongo_client[settings.mongo_db]
