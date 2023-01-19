from fastapi import APIRouter
from .schema import NewUserSchema, PublicUserSchema, UpdateUserSchema
from ...core.users.service import UserService

user_svc = UserService()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/"
, response_model=list[PublicUserSchema]
)
async def retrieve_all_users(
    email: str = None,
    name: str = None
    ):
    if not email and not name:
        return await user_svc.get_all_users()
    
    return await user_svc.get_users_by_id(email, name)


@router.get("/{user_id}/"
, response_model=PublicUserSchema
)
async def retrieve_user_by_id(user_id: str):
    print(user_id)
    return await user_svc.get_user(user_id)


@router.post("/"
, response_model=PublicUserSchema
)
async def create_user(user: NewUserSchema):
    return await user_svc.create_user(user)


@router.put("/{user_id}/"
, response_model=PublicUserSchema
)
async def update_user(user_id: str, user: UpdateUserSchema):
    return await user_svc.update_user(user_id, user)


@router.delete("/{user_id}/")
async def delete_user(user_id: str):
    return await user_svc.delete_user(user_id)

