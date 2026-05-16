from fastapi import FastAPI, Depends

from app.api.deps import check_authorization, require_permission
from app.api.routes.auth import auth_router
from app.api.routes.admin import admin_router
from app.api.routes.test_resources import test_resources_router
from app.api.routes.user import user_router
from app.db.session import get_db_session

app = FastAPI()
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(test_resources_router)

#
# @app.get("/test")
# async def test(
#     _: None = Depends(require_permission('admin_panel', 'read',))
# ):
#     return 200
