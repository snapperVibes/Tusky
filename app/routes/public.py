from os import path

from fastapi import APIRouter, Request
from fastapi.openapi.models import Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .api import room_details

_HERE = path.dirname(path.realpath(__file__))
t = Jinja2Templates(directory=path.join(_HERE, "..", "templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(r: Request):
    return t.TemplateResponse("root.html", {"request": r})


@router.get("/room/{roomcode}", response_class=HTMLResponse)
async def room(roomcode: str, req: Request, resp: Response):
    room_data = room_details(roomcode)
    resp.set_cookie(key="x", value="y")
    return t.TemplateResponse("room.html", {"request": req, "room": room_data})
