from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.scripts import db_patch_users, db_get_users, db_delete_user, db_get_permissions, check_ownership, \
    db_delete_permission, db_add_permission, db_patch_permission
from app.db.session import get_db_session_autocommit
from app.api.deps import require_permission
from app.schemas.permission_schema import PermissionAddSchema, PermissionEditSchema
from app.schemas.user_schema import UserRegisterSchema, UserWithIdSchema

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@admin_router.get('/user')
async def get_all_users(
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('admin_panel', 'read')),
):
    users = await db_get_users(session)
    return users


@admin_router.patch('/user')
async def edit_users(
        data: List[UserWithIdSchema],
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('admin_panel', 'update')),
):
    await db_patch_users(session, data)
    return {'status': 'ok'}


@admin_router.delete('/user')
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('admin_panel', 'delete')),
):
    await db_delete_user(session, user_id)
    return {'status': 'ok'}


@admin_router.get('/permission')
async def get_all_permissions(
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('admin_panel', 'read')),
):
    perm = await db_get_permissions(session)
    return perm


@admin_router.post('/permission')
async def add_permission(
        data: PermissionAddSchema,
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('admin_panel', 'create')),
):
    await db_add_permission(session, data)
    return {'status': 'ok'}


@admin_router.patch('/permission')
async def edit_permission(
        data: PermissionEditSchema,
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('admin_panel', 'update')),
):
    await db_patch_permission(session, data)
    return {'status': 'ok'}


@admin_router.delete('/permission')
async def delete_permission(
        permission_id: int,
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('admin_panel', 'delete')),
):
    await db_delete_permission(session, permission_id)
    return {'status': 'ok'}
