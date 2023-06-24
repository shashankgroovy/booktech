import redis

from booktech.utils.configurator import load_yaml_config


class Cache:
    """A wrapper around redis for easy access to cache"""

    config: dict
    client: redis.Redis

    def __init__(self):
        cfg = load_yaml_config()
        self.config = cfg.get("cache", {})

        if not self.config:
            raise Exception("Unable to connect to redis")

        self.client = redis.Redis(
            host=self.config["host"],
            port=self.config["port"],
            db=self.config["db"]
        )

    def get(self, key):
        """Syntactic sugar for getting a key's value"""
        return self.client.get(key)

    def set(self, key, value):
        """Syntactic sugar for setting a key-value pair"""
        return self.client.set(key, value)

    def delete(self, key):
        """Syntactic sugar for deleting a key"""
        return self.client.get(key)


# Initalize the default cache
cache = Cache()
