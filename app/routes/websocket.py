from fastapi import APIRouter, WebSocket

router = APIRouter()


@router.websocket("/ws")
async def ws_enter_room(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(data)


@router.websocket("/ws/room/{roomcode}")
async def ws_room(roomcode: str, ws: WebSocket):
    await ws.accept()
    while True:
        user = await ws.receive_text()
        await ws.send_text(f"Welcome, {user}")
