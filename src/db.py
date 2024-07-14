import logging

from config.config import cfg
from config.exceptions import UserNotFoundError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from schemas.user import User

logger = logging.getLogger(__name__)


class ClientDB:
    def __init__(self) -> None:
        self.client = MongoClient(cfg.DB_URI, server_api=ServerApi("1"))
        self.db_name = "yt2mp3"
        self.user_collection = "users"
        self.music_collection = "music"

    def list_databases(self) -> list[str]:
        return self.client.list_database_names()

    def list_collections(self, db_name: str) -> list[str]:
        return self.client[db_name].list_collection_names()

    def add_user(self, user: User) -> None:
        self.client[self.db_name][self.user_collection].insert_one(user.dict())

    def get_user(self, user_id: int) -> User:
        response = self.client[self.db_name][self.user_collection].find_one(
            {"user_id": user_id}
        )
        if response is None:
            logger.info(f"User not found: {user_id=}")
            raise UserNotFoundError("User not found")
        return User(**response)

    def get_users(self) -> list[User]:
        return [
            User(**user)
            for user in self.client[self.db_name][self.user_collection].find()
        ]

    def update_user(self, user: User) -> None:
        self.client[self.db_name][self.user_collection].update_one(
            {"user_id": user.user_id}, {"$set": user.dict(exclude_none=True)}
        )

    def disable_user(self, user_id: int) -> None:
        self.client[self.db_name][self.user_collection].update_one(
            {"user_id": user_id}, {"$set": {"active": False}}
        )


if __name__ == "__main__":
    db = ClientDB()
    user1 = User(
        username="test",
        user_id=12313,
        first_name="test",
        language_code="en",
    )
    db.add_user(user1)
    print(db.get_user(1))
