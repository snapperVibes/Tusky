from fastapi import FastAPI
from fastapi_operation_id import clean_ids

from app.routes import router

app = FastAPI()
app.include_router(router)
clean_ids(app)
