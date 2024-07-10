from abc import ABC, abstractmethod

from pydantic import UUID4

from src.users.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User):
        ...

    @abstractmethod
    async def search(self, id: UUID4):
        ...
