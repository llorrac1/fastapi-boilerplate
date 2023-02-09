from ..schema import BaseSchema

class NewUserSchema(BaseSchema):
    name: str
    email: str
    password: str


class UpdateUserSchema(BaseSchema):
    name: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False


class UserSchema(BaseSchema):
    id: str
    name: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False


class PublicUserSchema(BaseSchema):
    id: str
    name: str
    email: str
    is_active: bool = True
    is_superuser: bool = False


class UserInDBSchema(UserSchema):
    hashed_password: str

