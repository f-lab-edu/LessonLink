import redis

pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0, encoding="UTF-8", decode_responses=True)
redis_client = redis.Redis(connection_pool=pool)