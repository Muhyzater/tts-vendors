from redis import ConnectionPool, Redis
from redis.exceptions import BusyLoadingError, ConnectionError


class Cache(object):
    """
    Generaic cache wrapper

    args
    -------------

    host (str): cache DB host

    port (int): port number

    db (int): DB number
    """

    def __init__(self, host: str, port: int, db: int):

        # TODO: cast port and db to int beforehand
        _connection_pool = ConnectionPool(host=host, port=int(port), db=int(db))

        self._cache = Redis(connection_pool=_connection_pool)
        
    def exists(self, key: str) -> bool:
        """
        check if key exits in cache

        args
        -------------
        key (str): key to check against

        return
        -------------
        exist (bool)
        """

        try:

            if self._cache.exists(key):
                return True
            return False

        except (ConnectionError, BusyLoadingError):
            return False

    def get_value(self, key: str):
        """
        fetch value for given key from cache

        args
        -------------
        key (str): key to fetch

        return
        -------------
        cached_value (object)
        """

        try:

            return self._cache.get(key)

        except (ConnectionError, BusyLoadingError):

            return None

    def set_value(self, key: str, value, expire_time: int = None) -> bool:
        """
        insert value with given key to cache

        args
        -------------
        key (str): key for value

        value (object): value to be inserted

        expire_time (int): expire time in seconds

        return
        -------------
        inserted_sucessfully (bool)
        """
        # TODO: add timeout argument
        try:
            self._cache.set(name=key, value=value, ex=expire_time)
            return True
        except (ConnectionError, BusyLoadingError):
            return False

    def flushall(self) -> None:
        """
        clear cache
        """
        self._cache.flushall()
