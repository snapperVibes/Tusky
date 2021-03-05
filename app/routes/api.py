import base64
import hashlib
import random
from typing import Optional

import bcrypt

# Todo: Fix flanker 'symbol is unreachable'
from flanker.addresslib import address
from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc, insert

from app import (
    dependencies as dep,
    models as m,
)
from app.schema import RoomDetails, CreateUser

router = APIRouter()


def api(endpoint):
    return f"/api/v1/{endpoint}"


########################################################################################
# Room
def generate_room_code(length=5) -> str:
    return "".join(
        [random.choice("ABCDEFGHJKMNPQRSTUVWXYZ23456789") for i in range(length)]
    )


@router.post(api("room/create"), tags=["Room"])
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


@router.post(api("room/close/{code}"), tags=["Room"])
def close_room(code: str, s: Session = dep.get_session):
    # Todo: Validate user has authority to close room or that room is closable
    #  THIS CODE CANNOT MAKE IT TO PRODUCTION WITHOUT VALIDATION
    stmt = select(m.Room).filter_by(code=code, active=True)
    room = s.execute(stmt).scalar()
    print(room)
    room.active = False
    s.commit()
    return RoomDetails.from_orm(room)


@router.get(api("room/details/{code}"), tags=["Room"])
def room_details(code: str, s: Session = dep.get_session):
    q = s.query(m.Room).filter_by(code=code, active=True).order_by(desc("ts")).first()
    return RoomDetails(
        code=code,
        active=False if (q is None or not q.active) else True,
    )


########################################################################################
# User
@router.post(api("user/create"), tags=["User"])
def create_user(user: CreateUser, s: Session = dep.get_session):
    # Hash password of any length
    sha = hashlib.sha256(user.password.encode("utf-8")).digest()
    b64 = base64.b64encode(sha)
    hashed = bcrypt.hashpw(b64, bcrypt.gensalt(rounds=14))

    email = address.validate_address(user.email)

    # Generate user number
    q = (
        s.query(m.User.number)
        .filter_by(name=user.name)
        .order_by(desc("number"))
        .first()
    )
    if q is None:
        number = 1
    else:
        number = q.number + 1

    user_stmt = (
        insert(m.User)
        .values(name=user.name, key=hashed, number=number)
        .returning(m.User.id, m.User.number)
    )
    email_stmt = (
        insert(m.EmailAddress)
        .values(mailbox=email.mailbox, hostname=email.hostname)
        .returning(m.EmailAddress.id)
    )
    user_id, user_num = s.execute(user_stmt).first().id
    email_id = s.execute(email_stmt).first().id
    s.add(m.LinkUserToEmailAddresses(user=user_id, email_address=email_id))
    s.commit()
    return True
