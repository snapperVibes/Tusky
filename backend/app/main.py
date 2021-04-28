import uvicorn
from os import path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.routes import router


_HERE = path.dirname(path.realpath(__file__))


def init_app():
    app = FastAPI()
    app.include_router(router)

    origins = settings.BACKEND_CORS_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = init_app()


if __name__ == "__main__":
    # Run development server
    print("This is the development server.\nDO NOT USE IN PRODUCTION.")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
