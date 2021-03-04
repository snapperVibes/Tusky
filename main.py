import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import router

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("shutdown")
async def shutdown():
    print("Shutting down")


app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


if __name__ == "__main__":
    # Run development server
    print("This is the development server.\nDO NOT USE IN PRODUCTION.")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
