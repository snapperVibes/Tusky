from os import path

from fastapi import APIRouter, Request
from fastapi.openapi.models import Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import api
from app import dependencies as dep

_HERE = path.dirname(path.realpath(__file__))
t = Jinja2Templates(directory=path.join(_HERE, "..", "templates"))
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(req: Request):
    return t.TemplateResponse("root.html", {"request": req})


@router.get("/login", response_class=HTMLResponse)
async def login(req: Request):
    return t.TemplateResponse("login.html", {"request": req})


@router.get("/room/{roomcode}", response_class=HTMLResponse)
async def room(roomcode: str, req: Request, s: Session = dep.get_session):
    room_data = api.room_details(roomcode, s)
    return t.TemplateResponse("room.html", {"request": req, "room": room_data})
