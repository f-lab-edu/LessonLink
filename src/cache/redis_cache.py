import redis

pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, encoding="UTF-8", decode_responses=True)
redis_client = redis.Redis(connection_pool=pool)

class RedisCacheLoginFunction:
    def __init__(self):
        self.redis_client = redis_client

    def get_cached_access_token(self, role: str, id: str):
        return self.redis_client.get(f"user:{role}:{id}:access_token")
    
    def set_cached_access_token(self, role: str, id: str, access_token: str):
        self.redis_client.set(f"user:{role}:{id}:access_token", access_token, ex=60*60, nx=True)

    def set_cached_expire_time(self, role: str, id: str, ex_time: int):
        redis_client.expire(f"user:{role}:{id}:access_token", ex_time)