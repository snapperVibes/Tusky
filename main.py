import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from quiz import views

app = FastAPI()

@app.on_event("startup")
async def startup():
    # app.state.db = db.init_engine()
    app.mount("/static", StaticFiles(directory="quiz/static"), name="static")
    app.include_router(views.router)

if __name__ == "__main__":
    # Run development server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
