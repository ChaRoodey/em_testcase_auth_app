from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.db.session import get_db_session
from app.routes.deps import require_auth
from app.models.user_model import UserModel
from app.schemas.user_schema import UserResponseSchema

admin_router = APIRouter(
    prefix="/admin",
    # dependencies=[Depends(require_auth)],
)


@admin_router.get('/')
async def get_users(
        session=Depends(get_db_session)
):
    res = await session.execute(select(UserModel))
    users = res.scalars().all()
    return users


@admin_router.patch('/edit')
async def edit_user():
    return {'status': 'ok'}
