from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Cache(ABC, Generic[T]):
    @abstractmethod
    async def has(self, key: str) -> bool:
        ...

    @abstractmethod
    async def get(self, key: str, deserializer) -> T | None:
        ...

    @abstractmethod
    async def set(self, key: str, value: T, ttl_in_second: int):
        ...
