from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.user_model import UserModel

router = APIRouter()


@router.post('/login')
async def login(
        username: str,
        password: str,
        session: AsyncSession = Depends(get_db_session)
):
    try:
        res = await session.execute(select(UserModel).filter_by(email=username))
        user = res.scalars().first()
    except Exception as e:
        raise

    if not user:
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    if not password == user.password_hash:
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    # session_obj = await create_session(user.user_id, session)
    #
    # _set_session_cookie(response, str(session_obj.session_id))

    return {"success": True}


@router.post('/register')
async def register():
    ...
