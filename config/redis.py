import redis
from .config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)
