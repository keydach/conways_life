from fastapi import APIRouter
from . import cell

router = APIRouter()
router.include_router(cell.router, prefix='', tags=['Состоение'])
