import json
from redis import Redis, DataError
from functools import wraps


class RedisCache:
    def __init__(self, config):
        self.config = config
        self.conn = Redis(**self.config["redis"])

    def set_value(self, name, dict_value, ttl):
        json_value = json.dumps(dict_value)
        try:
            self.conn.set(name, json_value)
            if ttl > 0:
                self.conn.expire(name, ttl)
            return True
        except DataError as err:
            return False

    def get_value(self, name):
        js_value = self.conn.get(name)
        if js_value:
            dict_value = json.loads(js_value)
            return dict_value
        else:
            return None


def fetch_from_cache(name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config)
    ttl = cache_config['ttl']

    def cache_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_items = cache_conn.get_value(name)
            if cached_items:
                print('Достали из кэша!')
                return (cached_items)
            else:
                response = func(*args, **kwargs)
                if response:
                    print('Достали из БД!')
                    cache_conn.set_value(name, response, ttl)
                return response

        return wrapper

    return cache_required


def update_from_cache(name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config)
    ttl = cache_config['ttl']

    def cache_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cached_items = cache_conn.get_value(name)
            response = func(*args, **kwargs)
            if response:
                print('Достали из БД!')
                cache_conn.set_value(name, response, ttl)
                return response

        return wrapper

    return cache_required
