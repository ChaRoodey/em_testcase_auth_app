from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_permission
from app.db.scripts import check_ownership
from app.db.session import get_db_session_autocommit

test_cart_data = [
    {'id': 1, 'owner_id': 1},
    {'id': 2, 'owner_id': 2},
    {'id': 3, 'owner_id': 3},
    {'id': 5, 'owner_id': 6},
]
test_product_data = [
    {'id': 1, 'owner_id': 2, 'title': 'Водопроводная труба 2 метра'},
    {'id': 2, 'owner_id': 2, 'title': 'Краски гуашь'},
    {'id': 3, 'owner_id': 2, 'title': 'Фотоновый ускоритель'},
    {'id': 5, 'owner_id': 2, 'title': 'Вертолет'},
]

test_resources_router = APIRouter(
    prefix="/test_resources",
    tags=["test_resources"],
)


@test_resources_router.get('/cart')
async def get_cart_by_id(
        cart_id: int,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('cart', 'read')),
):
    owner_id = next(
        cart["owner_id"]
        for cart in test_cart_data
        if cart["id"] == cart_id
    )
    check_ownership(curr_user, owner_id)
    # cart = await db_get_cart(session, cart_id)
    return {'cart_id': cart_id}


@test_resources_router.post('/cart')
async def add_cart(
        data,
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('cart', 'create')),
):
    # await db_add_cart(session, data)
    return {'status': 'ok'}


@test_resources_router.patch('/cart')
async def edit_cart(
        cart_id: int,
        data: Dict = None,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('cart', 'update')),
):
    owner_id = next(
        cart["owner_id"]
        for cart in test_cart_data
        if cart["id"] == cart_id
    )
    check_ownership(curr_user, owner_id)
    # await db_patch_cart(session, [data])
    return {'status': 'ok'}


@test_resources_router.delete('/cart')
async def delete_cart(
        cart_id: int,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('cart', 'delete')),
):
    owner_id = next(
        cart["owner_id"]
        for cart in test_cart_data
        if cart["id"] == cart_id
    )
    check_ownership(curr_user, owner_id)
    # await db_delete_cart(session, cart_id)
    return {'status': 'ok'}


@test_resources_router.get('/product')
async def get_product_by_id(
        product_id: int,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('product', 'read')),
):
    owner_id = next(
        product["owner_id"]
        for product in test_product_data
        if product["id"] == product_id
    )
    check_ownership(curr_user, owner_id)
    # user = await db_get_product(session, product_id)
    return {'status': 'ok'}


@test_resources_router.post('/product')
async def add_product(
        data,
        session: AsyncSession = Depends(get_db_session_autocommit),
        _: None = Depends(require_permission('product', 'create')),
):
    # await db_add_product(session, data)
    return {'status': 'ok'}


@test_resources_router.patch('/product')
async def edit_product(
        product_id: int,
        data: Dict = None,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('product', 'update')),
):
    owner_id = next(
        product["owner_id"]
        for product in test_product_data
        if product["id"] == product_id
    )
    check_ownership(curr_user, owner_id)
    # await db_patch_products(session, [data])
    return {'status': 'ok'}


@test_resources_router.delete('/product')
async def delete_product(
        product_id: int,
        session: AsyncSession = Depends(get_db_session_autocommit),
        curr_user: Dict = Depends(require_permission('product', 'delete')),
):
    owner_id = next(
        product["owner_id"]
        for product in test_product_data
        if product["id"] == product_id
    )
    check_ownership(curr_user, owner_id)
    # await db_delete_product(session, product_id)
    return {'status': 'ok'}
