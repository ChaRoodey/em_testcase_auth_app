import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta

from app.core.config import settings
from app.models.session_model import SessionModel


async def create_session(user_id: int, session: AsyncSession) -> SessionModel:
    expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.SESSION_TTL_HOURS)

    session_obj = SessionModel(
        user_id=user_id,
        expires_at=expires_at,
    )

    session.add(session_obj)
    await session.flush()
    await session.refresh(session_obj)

    return session_obj


async def get_session(session_id: uuid.UUID, session: AsyncSession) -> SessionModel:
    res = await session.execute(select(SessionModel).filter_by(id=session_id))
    return res.scalar_one_or_none()


async def delete_session(session_obj, session: AsyncSession) -> None:
    await session.delete(session_obj)
