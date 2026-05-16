from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_permission
from app.db.base import Base
from app.db.scripts import db_patch_users, db_get_users, db_delete_user, check_ownership
from app.db.session import get_db_session_autocommit
from app.schemas.user_schema import UserWithIdSchema

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(require_auth)],
)


@user_router.get('/')
async def get_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('profile', 'read')),
):
    check_ownership(curr_user, user_id)
    user = await db_get_users(session, user_id)
    return user


@user_router.patch('/')
async def edit_user(
        data: UserWithIdSchema,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('profile', 'update')),
):
    check_ownership(curr_user, data.id)
    await db_patch_users(session, [data])
    return {'status': 'ok'}


@user_router.delete('/')
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('profile', 'delete')),
):
    check_ownership(curr_user, user_id)
    await db_delete_user(session, user_id)
    return {'status': 'ok'}
