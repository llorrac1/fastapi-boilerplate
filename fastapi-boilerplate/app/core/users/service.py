from fastapi import HTTPException, status
from .schema import UserDto, NewUserDto, UserInDBDto
from ...api.users.schema import PublicUserSchema, NewUserSchema
from typing import Optional
from pydantic import Field
import uuid
import hashlib

from ...db.redis.users.db import UserDB


class UserService:
    def __init__(self, db = UserDB(), cache = None):
        self.__db = db
        self.__cache = cache if cache else None


    async def create_user(self, user: NewUserSchema) -> PublicUserSchema:
        user.password = hashlib.sha256(user.password.encode()).hexdigest()
        user = UserDto(**user.dict(),
            id = str(uuid.uuid4().hex),
            is_active = True,
            is_superuser = False
            )
        print(user)

        try: 
            saved_user = await self.__db.create_user(user)
            return PublicUserSchema(**saved_user)
            # return True

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create user")


    async def get_user(self, user_id: str) -> Optional[PublicUserSchema] or None:
        try: 
            user = await self.__db.get_user(user_id)

            if user: 
                print(user)
                return PublicUserSchema(**user)

            return None

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")


    async def get_all_users(self): 
        try: 
            users = await self.__db.get_all_users() 
            return [PublicUserSchema(**user) for user in users]
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
    
    async def get_users_by_id(self, email: str = None, name: str = None) -> list[PublicUserSchema]:
        try: 
            users = await self.__db.get_users(name=name, email=email)

            if users:
                print(users)

                return [PublicUserSchema(**user) for user in users]

            return None

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not retrieve users using that identifier")


    async def update_user(self, user_id: str, user: UserDto) -> PublicUserSchema:
        try: 
            print("user to update: ", user)
            to_update = UserDto(**user.dict(), id = user_id)
            updated_user = await self.__db.update_user(user_id=user_id, user=to_update)
            
            if updated_user: 
                return PublicUserSchema(**updated_user)

            return None

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update user")


    async def delete_user(self, user_id: str) -> bool:
        try:
            deleted = await self.__db.delete_user(user_id)
            
            if deleted:
                if self.__cache is not None:
                    await self.__cache.delete_user(user_id)
                return True

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not find user to delete")
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not delete user")