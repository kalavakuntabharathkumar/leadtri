from functools import lru_cache
from pymongo import MongoClient
import redis
from .config import MONGODB_URL, MONGODB_DATABASE, REDIS_URL

@lru_cache
def mongo_db():
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=1500)
    return client[MONGODB_DATABASE]

@lru_cache
def redis_client():
    return redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)

def cache_key(content_id: str) -> str:
    return f"content:v1:{content_id}"
