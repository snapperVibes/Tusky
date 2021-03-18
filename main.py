import uvicorn

from app import init_app

app = init_app()


if __name__ == "__main__":
    # Run development server
    print("This is the development server.\nDO NOT USE IN PRODUCTION.")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
