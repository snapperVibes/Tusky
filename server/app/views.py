from os import path

from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

HERE = path.dirname(path.realpath(__file__))
t = Jinja2Templates(directory=path.join(HERE, "templates"))


@router.get("/", response_class=HTMLResponse)
async def root(r: Request):
    return t.TemplateResponse("home.html", {"request": r})
