from os import path
from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Query, Request, WebSocket, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

HERE = path.dirname(path.realpath(__file__))
t = Jinja2Templates(directory=path.join(HERE, "templates"))


@router.get("/", response_class=HTMLResponse)
async def root(r: Request):
    return t.TemplateResponse("home.html", {"request": r})


async def get_cookie_or_token(
    ws: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@router.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    ws: WebSocket,
    item_id: str,
    q: Optional[int] = None,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Session cookie or query token value is: {cookie_or_token}")
        if q is not None:
            await ws.send_text(f"Query parameter q is: {q}")
        await ws.send_text(f"Message text was: {data}, for item ID: {item_id}")
