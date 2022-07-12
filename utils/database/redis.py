import redis
import json


class Redis:

    server = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def hsetex(self, name, key, value, ex=None):
        self.server.hset(name, key, value)
        if ex:
            self.server.expire(name, ex)

    def set_json(self, key, value, ex=None, px=None, nx=None, xx=None):
        value = json.dumps(value)
        return self.server.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get_json(self, key):
        value = self.server.get(key)
        if value:
            value = json.loads(value)
        return value
