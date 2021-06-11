from fastapi import Depends
from fastapi.routing import APIRouter

from app import dependencies as deps
from app.core import settings

###################################################################################################
user_router = APIRouter()


###################################################################################################
login_router = APIRouter(prefix="/login")


@login_router.get("/access-token")
def get_access_token():
    return


###################################################################################################
router = APIRouter(prefix=settings.API_STR_V1)
router.include_router(user_router)
router.include_router(login_router)


@router.get("/")
async def root():
    return 'Hello!'


