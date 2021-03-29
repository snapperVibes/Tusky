from fastapi import APIRouter

view_router = APIRouter()


@view_router.get("/")
def home():
    return {"msg": "Hello, world"}
