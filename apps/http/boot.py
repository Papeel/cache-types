import inject
from inject import Binder
import redis
import mariadb

from src.users.domain.repository import UserRepository
from src.users.infraestructure.cache.redis.cache import UserRedisCache
from src.users.infraestructure.db.mariadb.repository import UserMariaDBRepository


class Boot:
    def __init__(self):
        if not inject.is_configured():
            inject.configure(self.configure)

    def configure(self, binder: Binder):
        redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        mariadb_client = mariadb.connect(
            user="juan", password="password", host="localhost", database="my_project"
        )
        user_mariadb_repository = UserMariaDBRepository(client=mariadb_client)
        user_redis_repository = UserRedisCache(
            client=redis_client, repository=user_mariadb_repository
        )
        binder.bind(UserRepository, user_redis_repository)

    @staticmethod
    def get(x):
        return inject.instance(x)
