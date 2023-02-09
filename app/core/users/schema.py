from ..schema import BaseDto


class NewUserDto(BaseDto):
    name: str
    email: str
    password: str


class UserDto(BaseDto):
    id: str
    name: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False


class UserInDBDto(UserDto):
    hashed_password: str

