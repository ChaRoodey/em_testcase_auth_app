import uuid
from datetime import datetime, timezone

from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.session import get_session
from app.db.session import get_db_session


async def require_auth(
        request: Request,
        session: AsyncSession = Depends(get_db_session),
):
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    print(f'{session_id=}')

    if not session_id:
        raise HTTPException(status_code=401, detail='Not authenticated')

    try:
        session_uuid = uuid.UUID(session_id)
        print(f'{session_uuid=}')
    except ValueError:
        raise HTTPException(status_code=401, detail='Invalid session id')

    session_obj = await get_session(session_uuid, session)

    if not session_obj:
        raise HTTPException(status_code=401, detail='Session not found')

    if session_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail='Session expired')

    return session_obj.user_id
