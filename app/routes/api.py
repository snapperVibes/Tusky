from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc

from app import (
    dependencies as dep,
    models as m,
)
from app.schema import RoomDetails

router = APIRouter()


def api(endpoint):
    return f"/api/v1/{endpoint}"


# Todo: some sort of refactoring so I can call api.room_details()
@router.get(api("room/details/{code}"), tags=["Room"])
def room_details(code: str, s: Session = dep.get_session):
    q = s.query(m.Room).filter_by(code=code, active=True).order_by(desc("ts")).first()
    return RoomDetails(
        code=code,
        active=False if (q is None or not q.active) else True,
    )


@router.get(api("room/close/{code}"), tags=["Room"])
def close_room(code: str, s: Session = dep.get_session):
    # Todo: Validate user has authority to close room or that room is closable
    #  THIS CODE CANNOT MAKE IT TO PRODUCTION WITHOUT VALIDATION
    stmt = select(m.Room).filter_by(code=code, active=True)
    room = s.execute(stmt).scalar()
    print(room)
    room.active = False
    s.commit()
    return RoomDetails.from_orm(room)


@router.get(api("room/create"), tags=["Room"])
def create_room(s: Session = dep.get_session) -> RoomDetails:
    while True:
        try:
            room = m.Room(code=m.generate_room_code(), active=True)
            s.add(room)
            s.commit()
            # Todo: actual url
            return RoomDetails.from_orm(room)
        except IntegrityError:
            # Recursively create room until a room code that has not been taken is choosen
            return create_room()
