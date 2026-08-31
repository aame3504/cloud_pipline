import redis

from app.config import REDIS_URL


redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


def check_redis_connection() -> bool:
    return bool(
        redis_client.ping()
    )