import redis
import json


class Redis:

    server = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def hsetex(self, name, key, value, ex=None):
        """
        Set the value to a key with expiration time, grouped by name
        If key already exists, it is overwritten, regardless of its type.

        Args:
            name (str): hash name
            key (str): hash key
            value (str): hash value
            ex (int): expire time in seconds
        """

        self.server.hset(name, key, value)
        if ex:
            self.server.expire(name, ex)

    def set_json(self, key, value, ex=None, px=None, nx=None, xx=None) -> bool:
        """
        Set json value to key
        Args:
            key (str): key
            value (str): value
            ex (int): sets an expiry flag on key in seconds.
            px (int): sets an expiry flag on key in milliseconds.
            nx (bool): if set to True, set the key if it does not exist.
            xx (bool): if set to True, set the key only if it already exists.

        Returns:
            (bool): True if key was set, False if key already exists
        """

        value = json.dumps(value)
        return self.server.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get_json(self, key) -> dict:
        """
        Get json value from key and return as dict or None if key does not exist
        Args:
            key (str): key

        Returns:
            (dict): value or None if key does not exist
        """

        value = self.server.get(key)
        if value:
            value = json.loads(value)
        return value
