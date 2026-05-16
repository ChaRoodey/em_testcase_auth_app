from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.session import create_session, delete_session
from app.db.session import get_db_session_autocommit
from app.models.user_model import UserModel
from app.core.security import security
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema
from app.models.session_model import SessionModel

auth_router = APIRouter(
    tags=["auth"],
)


def _set_session_cookie(response: Response, token: str):
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite="lax",
        max_age=settings.SESSION_TTL_HOURS * 3600,
        domain=settings.SESSION_COOKIE_DOMAIN,
    )


@auth_router.post('/login')
async def login(
        data: UserLoginSchema,
        response: Response,
        session: AsyncSession = Depends(get_db_session_autocommit)
):
    res = await session.execute(select(UserModel).filter_by(email=data.email))
    user = res.scalars().one_or_none()

    # if not user.is_active:
    #     raise HTTPException(status_code=401, detail="User inactive or deleted")

    if not user or not user.is_active or not security.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong login/password")

    session_obj = await create_session(user.id, session)

    _set_session_cookie(response, str(session_obj.id))

    return {"success": True}


@auth_router.post('/register')
async def register(
        req: UserRegisterSchema,
        session: AsyncSession = Depends(get_db_session_autocommit)
):
    data = req.model_dump()
    data['password'] = security.hash_password(data['password'])

    new_user = UserModel(**data)
    session.add(new_user)

    return {"success": True}


@auth_router.post("/logout")
async def logout(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_db_session_autocommit)
):
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if session_id:
        session_obj = await session.get(SessionModel, session_id)
        if session_obj:
            await delete_session(session_obj, session)

    response.delete_cookie(settings.SESSION_COOKIE_NAME)
    return {"success": True}
