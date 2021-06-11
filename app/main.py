import uvicorn

from fastapi import FastAPI

from app.routes import router


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


app = init_app()
