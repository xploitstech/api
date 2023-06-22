import os
from contextlib import asynccontextmanager

from redis import ConnectionPool, Redis
from redis import asyncio as aioredis

from .settings import ENGINE_REDIS_URI

REDIS_CONFIG_CORS_KEY = "configs:cors:engineapi"


def create_redis_client() -> Redis:
    rc_pool = ConnectionPool.from_url(
        url=ENGINE_REDIS_URI, max_connections=10, decode_responses=True
    )
    return Redis(connection_pool=rc_pool)


rc_client = create_redis_client()


def create_async_redis_client() -> Redis:
    rc_pool_async: ConnectionPool = aioredis.ConnectionPool.from_url(
        url=ENGINE_REDIS_URI, max_connections=10, decode_responses=True
    )

    return aioredis.Redis(connection_pool=rc_pool_async)


rc_client_async = create_async_redis_client()


@asynccontextmanager
async def yield_rc_async_session():
    try:
        yield rc_client_async
    finally:
        await rc_client_async.close()
