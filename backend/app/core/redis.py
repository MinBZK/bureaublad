from functools import lru_cache

from redis.asyncio import Redis

from app.core.config import settings


@lru_cache
def get_redis_client() -> Redis:
    """Create and cache a Redis client instance."""
    return Redis.from_url(url=str(settings.REDIS_URL), decode_responses=True)  # pyright: ignore[reportUnknownMemberType]
