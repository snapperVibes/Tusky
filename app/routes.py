from os import path
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Query, Request, WebSocket, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

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


@router.get("/room/{roomcode}", response_class=HTMLResponse)
async def room(roomcode: str, r: Request):
    return t.TemplateResponse(
        "room.html",
        {
            "request": r,
            "roomcode": roomcode.upper(),
            "room_text": "This is the room text"
        }
    )


@router.websocket("/ws/room/{roomcode}")
async def ws_room(roomcode: str, ws: WebSocket):
    await ws.accept()
    while True:
        user = await ws.receive_text()
        await ws.send_text(f"Welcome, {user}")


def api(endpoint):
    return f"/api/v1/{endpoint}"


# @router.get(api("room/details/{code}"))
# def room_details(code: str):
#     return db.rooms.get(code.upper(), {"active": False})
#
#
# @router.get(api("room/create"))
# def create_room():
#     return db.new_room()


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
