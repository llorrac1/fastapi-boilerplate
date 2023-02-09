from sqlmodel import SQLModel, Field, create_engine, Session, select 

from typing import Optional

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(None, index=True)
    password: str = None
    email: str = Field(None, index=True)
    is_active: str = None
    is_superuser: str = None


class Users(SQLModel, table=True): 
    id: str = Field(primary_key=True)
    name: str = Field(None, index=True)
    password: str = None
    email: str = Field(None, index=True)
    is_active: str = None
    is_superuser: str = None


sqlite_file_name = "sqlite.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()


class UserDB:
    def __init__(self):
        self.__db = Session(engine)
        create_db_and_tables()

    async def create_user(self, data: Users) -> User:
        user = Users(**data)
        # print(user)
        self.__db.add(user)
        self.__db.commit()
        self.__db.refresh(user)
        return user.dict()


    async def get_user(self, user_id: str) -> Users or None:
        user = self.__db.get(Users, user_id)
        return user.dict()


    async def get_all_users(self) -> list[Users]:
        users = self.__db.exec(select(Users))
        return [u.dict() for u in users]


    async def get_users_by_id(self, email: str = None, name: str = None) -> list[Users]:
        if email and name:
            users = self.__db.exec(select(Users).where(Users.email == email).where(Users.name == name)).all()
            return [u.dict() for u in users]

        elif email:
            users = self.__db.exec(select(Users).where(Users.email == email)).all()
            return [u.dict() for u in users]

        elif name:
            users = self.__db.exec(select(Users).where(Users.name == name)).all()
            return [u.dict() for u in users]

        else:
            return []

    async def update_user(self, user_id: str, data: Users) -> Users or None:
        query = self.__db.exec(select(Users).where(Users.id == user_id))
        user = query.one()
        if user:
            updated = Users(**data)
            user.name = updated.name
            user.password = updated.password
            user.email = updated.email
            user.is_active = updated.is_active
            user.is_superuser = updated.is_superuser
            self.__db.add(user)
            self.__db.commit()
            self.__db.refresh(user)
            return user.dict()

        return None

    async def delete_user(self, user_id: str) -> bool:
        user = self.__db.get(Users, user_id)
        if user:
            self.__db.delete(user)
            self.__db.commit()
            return True

        return False