from ...redis.db import User
from typing import Optional


class UserDB:
    def __init__(self):
        pass
        
    async def create_user(self, user: User) -> dict:
        try:
            user = User(**user.dict())
            user.pk = user.id
            user.check()
            user.save()
            return user.dict()
        except Exception as e:
            print(e)
            return False


    async def get_user(self, user_id: str) -> Optional[dict]:
        try:
            user = User.get(user_id)
            if not user:
                user = User.find(User.id == user_id).first()
            return user.dict()
        except Exception as e:
            print(e)
            return False


    async def get_all_users(self) -> list[dict]:
        try: 
            users = User.all_pks()
            users = [User.get(u).dict() for u in users]
            return users


        except Exception as e: 
            return None



    async def get_users(self, name = None, email = None) -> list[dict]:
        try: 

            if name and email:
                try:
                    users = User.find(
                        (User.name == name) or 
                        (User.email == email)
                        ).all()
                    return [user.dict() for user in users]
                except Exception as e:
                    print(e)
                    return False

            if name:
                try:
                    users = User.find(User.name == name).all()
                    return [user.dict() for user in users]
                except Exception as e:
                    print(e)
                    return False

            if email:
                try:
                    users = User.find(User.email == email).all()
                    return [user.dict() for user in users]
                except Exception as e:
                    print(e)
                    return False

            return None

        except Exception as e:
            print(e)
            return False


    async def update_user(self, user_id: str, user: User) -> dict:

        try: 
            user_to_update = User.find(User.id == user_id).first()

        except:
            print("redis failed to find user with id: ", user_id)
            return False
        
        try:
            if user_to_update:
                updated_user = User(**user.dict())
                user_to_update.update(**updated_user.dict())
                user_to_update.check()
                user_to_update.save()
            return user_to_update.dict()

        except Exception as e:
            print(e)
            return False


    async def batch_update_users(self, users: list[User]) -> list[dict]:
        try:
            users_to_update = [User(**user.dict()) for user in users]
            User.update(users_to_update)
            return [user.dict() for user in users_to_update]
        except Exception as e:
            print(e)
            return False


    async def delete_user(self, user_id: str) -> bool:
        try:
            user = User.find(User.id == user_id).first()
            if not user:
                user = User.get(user_id)
            if user:
                user.delete(user.pk)
            return True
        except Exception as e:
            print(e)
            return False