from typing import List, Dict

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import security
from app.models.permission_model import PermissionsModel
from app.models.resource_model import ResourcesModel
from app.models.user_model import UserModel
from app.schemas.permission_schema import PermissionEditSchema, PermissionAddSchema
from app.schemas.user_schema import UserRegisterSchema, UserWithIdSchema


def check_ownership(user: Dict, owner_id: int) -> None:
    if user['access_level'] == 'all':
        return

    if user['access_level'] == 'one' and user['user_id'] == owner_id:
        return

    raise HTTPException(403)


async def db_get_users(
        session: AsyncSession,
        user_id: int | None = None,
):
    if user_id is None:
        users = await session.execute(select(UserModel))
        return users.scalars().all()

    user = await session.get(UserModel, user_id)
    return user


async def db_patch_users(
        session: AsyncSession,
        new_users: List[UserWithIdSchema],
) -> None:
    for new_user in new_users:
        curr_user = await session.get(UserModel, new_user.id)

        if not curr_user:
            raise HTTPException(404, 'User not found')

        update_data = new_user.model_dump(exclude_unset=True)
        update_data['password'] = security.hash_password(update_data['password'])
        for field, value in update_data.items():
            setattr(curr_user, field, value)


async def db_delete_user(
        session: AsyncSession,
        user_id: int,
) -> None:
    user = await session.get(UserModel, user_id)

    if not user:
        raise HTTPException(404, 'User not found')

    if not user.is_active:
        raise HTTPException(409, 'User already deactivated')

    user.is_active = False


async def db_get_permissions_by_user_id(
        session: AsyncSession,
        curr_user_id: int,
        resource: str,
):
    stmt = (
        select(PermissionsModel)
        .join(
            UserModel,
            UserModel.role_id == PermissionsModel.role_id
        )
        .join(
            ResourcesModel,
            ResourcesModel.id == PermissionsModel.resource_id
        )
        .where(
            UserModel.id == curr_user_id,
            ResourcesModel.title == resource
        )
    )

    result = await session.execute(stmt)
    return result.scalars().all()[0]


async def db_get_permissions(
        session: AsyncSession,
):
    users = await session.execute(select(UserModel))
    return users.scalars().all()


async def db_add_permission(
        session: AsyncSession,
        new_permission: PermissionAddSchema,
):
    new_user = PermissionsModel(**new_permission.model_dump(exclude_unset=True))
    session.add(new_user)


async def db_patch_permission(
        session: AsyncSession,
        new_permission: PermissionEditSchema,
) -> None:
    curr_permission = await session.get(PermissionsModel, new_permission.id)

    if not curr_permission:
        raise HTTPException(404, 'Permission not found')

    update_data = new_permission.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(curr_permission, field, value)


async def db_delete_permission(
        session: AsyncSession,
        permission_id: int,
) -> None:
    permission = await session.get(PermissionsModel, permission_id)

    if not permission:
        raise HTTPException(404, 'Permission not found')

    await session.delete(permission)
