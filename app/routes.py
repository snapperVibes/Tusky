from os import path

from fastapi import APIRouter, Cookie, Depends, Query, Request, WebSocket, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import insert, update, delete, text, desc
from . import db

router = APIRouter()

HERE = path.dirname(path.realpath(__file__))
t = Jinja2Templates(directory=path.join(HERE, "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(r: Request):
    return t.TemplateResponse("home.html", {"request": r})


@router.websocket("/ws")
async def ws_enter_room(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(data)


@router.get("/room/{roomcode}")
async def room(roomcode: str):
    room_data = room_details(roomcode)
    return room_data


@router.websocket("/ws/room/{roomcode}")
async def ws_room(roomcode: str, ws: WebSocket):
    await ws.accept()
    while True:
        user = await ws.receive_text()
        await ws.send_text(f"Welcome, {user}")


def api(endpoint):
    return f"/api/v1/{endpoint}"


class RoomDetails(BaseModel):
    code: str
    active: bool


# Todo: some sort of refactoring so I can call api.room_details()
@router.get(api("room/details/{code}"))
def room_details(code: str):
    with db.Session() as s:
        q = s.query(db.Room).filter_by(code=code, active=True).order_by(desc("ts")).first()
        return RoomDetails(
            code=code,
            active=False if (q is None or not q.active) else True,
        )


@router.get(api("room/close/{code}"))
def close_room(code: str):
    # Todo: Validate user has authority to close room or that room is closable
    pass


@router.get(api("room/create"))
def create_room():
    while True:
        try:
            with db.Session() as s:
                room = db.Room(code=db.generate_room_code(), active=True)
                s.add(room)
                s.commit()
                code = room.code
            # Todo: actual url
            return RoomDetails(
                code=code,
                active=False if (s in None or not s.active) else True
            )
        except IntegrityError:
            print("Oh no, trying again")
            return create_room()


# @router.get("/example_home", response_class=HTMLResponse)
# async def get_cookie_or_token(
#     ws: WebSocket,
#     session: Optional[str] = Cookie(None),
#     token: Optional[str] = Query(None),
# ):
#     if session is None and token is None:
#         await ws.close(code=status.WS_1008_POLICY_VIOLATION)
#     return session or token


# @router.get("/example", response_class=HTMLResponse)
# async def root(r: Request):
#     return t.TemplateResponse("home.html", {"request": r})
#
#
# @router.websocket("/example_items/{item_id}/ws")
# async def websocket_endpoint(
#     ws: WebSocket,
#     item_id: str,
#     q: Optional[int] = None,
#     cookie_or_token: str = Depends(get_cookie_or_token),
# ):
#     await ws.accept()
#     while True:
#         data = await ws.receive_text()
#         await ws.send_text(f"Session cookie or query token value is: {cookie_or_token}")
#         if q is not None:
#             await ws.send_text(f"Query parameter q is: {q}")
#         await ws.send_text(f"Message text was: {data}, for item ID: {item_id}")
