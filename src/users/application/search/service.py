import inject
from pydantic import UUID4


from src.users.domain.exceptions import UserDoesntExists
from src.users.domain.repository import UserRepository
from src.users.domain.user import User


class UserSearcher:
    repository: UserRepository

    @inject.autoparams()
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def __call__(self, id: UUID4) -> list[User]:
        user = await self.repository.search(id)
        if user is None:
            raise UserDoesntExists()
        return user
