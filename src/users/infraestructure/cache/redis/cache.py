from pydantic import UUID4
from redis import Redis
from src.users.domain.user import User
from src.users.domain.repository import UserRepository


class UserRedisCache(UserRepository):
    client: Redis
    repository: UserRepository

    def __init__(self, client: Redis, repository: UserRepository) -> None:
        self.client = client
        self.repository = repository

    async def save(self, user: User):
        await self.repository.save(user)

    async def search(self, id: UUID4):
        if await self._has(id.hex):
            return await self._get(id.hex, lambda obj: User.model_validate_json(obj))

        user = await self.repository.search(id)
        await self._set(id.hex, user.model_dump_json(), 60)
        return user

    async def _has(self, key: str) -> bool:
        return self.client.exists(key)

    async def _get(self, key: str, deserializer) -> User | None:
        response = self.client.get(key)
        if response is None:
            return None
        return deserializer(response)

    async def _set(self, key: str, value: str, ttl_in_second: int):
        self.client.set(name=key, value=value, ex=ttl_in_second)
