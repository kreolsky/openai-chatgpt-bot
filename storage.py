import redis
import datetime
import json

class RedisConnection:
    def __init__(self, url):
        self.url = url

    def __enter__(self):
        self.redis = redis.Redis.from_url(self.url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis.close()

    def delete(self, key):
        self.redis.delete(key)

    def list_push(self, key, value):
        self.redis.rpush(key, json.dumps(value))

    def list_range(self, key):
        return [json.loads(item) for item in self.redis.lrange(key, 0, -1)]

def user_key(func):
    def wrapper(self, user_id, *args, **kwargs):
        key = f"user:{user_id}:history"
        return func(self, key, *args, **kwargs)
    return wrapper

class UserManager:
    def __init__(self, redis_conn: RedisConnection):
        self.redis_conn = redis_conn

    @user_key
    def add_message(self, key, role, text):
        message = {
            "role": role,
            "text": text,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self.redis_conn.list_push(key, message)

    @user_key
    def get_history(self, key):
        return self.redis_conn.list_range(key)

    @user_key
    def clear_history(self, key):
        self.redis_conn.delete(key)


# class RedisConnection:
#     def __init__(self, url):
#         self.redis = redis.Redis.from_url(url)
#
#     def set(self, key, value):
#         self.redis.set(key, json.dumps(value))
#
#     def get(self, key):
#         value = self.redis.get(key)
#         return json.loads(value) if value else None
#
#     def delete(self, key):
#         self.redis.delete(key)
#
#     def list_push(self, key, value):
#         self.redis.rpush(key, json.dumps(value))
#
#     def list_range(self, key):
#         return [json.loads(item) for item in self.redis.lrange(key, 0, -1)]
#
# class UserManager:
#     def __init__(self, redis_conn: RedisConnection):
#         self.redis_conn = redis_conn
#
#     def _user_key(self, user_id):
#         return f"user:{user_id}:history"
#
#     def add_message(self, user_id, role, text):
#         key = self._user_key(user_id)
#         message = {
#             "role": role,
#             "text": text,
#             "timestamp": datetime.datetime.utcnow().isoformat()
#         }
#         self.redis_conn.list_push(key, message)
#
#     def get_history(self, user_id):
#         key = self._user_key(user_id)
#         return self.redis_conn.list_range(key)
#
#     def clear_history(self, user_id):
#         key = self._user_key(user_id)
#         self.redis_conn.delete(key)
