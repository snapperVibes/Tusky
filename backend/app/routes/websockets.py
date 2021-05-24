from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from . import _depends as deps

router = APIRouter()


# @router.websocket("/hello")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#          data = await websocket.receive_text()
#          await websocket.send_text(f"Message text was: {data}")

@router.websocket("/session/get_responses")
async def get_responses_by_session(
    websocket: WebSocket,
    *,
    db: Session = Depends(deps.get_db),
    session_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    session = crud.quiz_session.get(db, id=session_id)
    if session.room.owner_id != current_user.id:
        raise HTTPException(
            status_code=400, detail="You can only view responses to your own sessions."
        )
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
