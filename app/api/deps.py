import uuid
from datetime import datetime, timezone

from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.session import get_session
from app.db.scripts import db_get_permissions_by_user_id
from app.db.session import get_db_session


def require_permission(resource: str, action: str):
    async def predicate(
            request: Request,
            session: AsyncSession = Depends(get_db_session),
    ):
        user_id = await check_authentication(request, session)

        access_level = await check_authorization(session, user_id, resource, action)

        return {
            'user_id': user_id,
            'access_level': access_level
        }

    return predicate


async def check_authentication(
        request: Request,
        session: AsyncSession
):
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)

    if not session_id:
        raise HTTPException(status_code=401, detail='Not authenticated')

    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        raise HTTPException(status_code=401, detail='Invalid session id')

    session_obj = await get_session(session_uuid, session)

    if not session_obj:
        raise HTTPException(status_code=401, detail='Session not found')

    if session_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail='Session expired')

    return session_obj.user_id


async def check_authorization(
        session: AsyncSession,
        user_id: int,
        resource: str,
        action: str,
):
    permission = await db_get_permissions_by_user_id(session, user_id, resource)

    if not permission:
        raise HTTPException(status_code=401, detail='Permission not found')

    if getattr(permission, 'can_all_' + action):
        return 'all'
    elif getattr(permission, 'can_' + action):
        return 'one'

    raise HTTPException(403)

# async def require_auth(
#         request: Request,
#         session: AsyncSession = Depends(get_db_session),
# ):
#     session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
#
#     if not session_id:
#         raise HTTPException(status_code=401, detail='Not authenticated')
#
#     try:
#         session_uuid = uuid.UUID(session_id)
#     except ValueError:
#         raise HTTPException(status_code=401, detail='Invalid session id')
#
#     session_obj = await get_session(session_uuid, session)
#
#     if not session_obj:
#         raise HTTPException(status_code=401, detail='Session not found')
#
#     if session_obj.expires_at < datetime.now(timezone.utc):
#         raise HTTPException(status_code=401, detail='Session expired')
#
#     user_roles = await db_get_permissions_by_user_id(session, session_obj.user_id)
#
#     return user_roles
