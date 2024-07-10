from asyncio import sleep
from dataclasses import dataclass
from mariadb.connections import Connection
from mariadb.cursors import Cursor
from pydantic import UUID4

from src.users.domain.repository import UserRepository
from src.users.domain.user import User


@dataclass
class UserMariaDBRepository(UserRepository):
    client: Connection

    async def save(self, user: User):
        cur: Cursor = self.client.cursor()
        query = """
        INSERT INTO users (id, name, email)
        VALUES(
            ?,
            ?,
            ?
        );
        """
        cur.execute(query, (user.id.hex, user.name, user.email))
        self.client.commit()

    async def search(self, id: UUID4):
        cur: Cursor = self.client.cursor()
        query = "SELECT id, name, email FROM users WHERE id = ?;"
        user = None
        cur.execute(query, (id.hex,))
        for user_id, name, email in cur:
            user = User.model_validate({"id": user_id, "name": name, "email": email})
        await sleep(3)
        return user
