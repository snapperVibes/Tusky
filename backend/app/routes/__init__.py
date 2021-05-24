from fastapi import APIRouter

from app.core import settings
from app.routes.login import router as login_router
from app.routes.quizzes import router as quiz_router
from app.routes.rooms import router as room_router
from app.routes.users import router as user_router
from app.routes.quiz_sessions import router as session_router
from app.routes.websockets import router as websocket_router

router = APIRouter(prefix=settings.API_V1_STR)
router.include_router(login_router)
router.include_router(quiz_router)
router.include_router(room_router)
router.include_router(user_router)
router.include_router(session_router)
router.include_router(websocket_router)


# Sets a custom operation_id for each route.
#   The operation id is used when generating the OpenAPI document.
#   Code generation (tusky/scripts/run-codegen.sh) uses
#   the operation_id when creating functions.
#
#   For example, without this block of code,
#   the Javascript function quizApi.update
#   would be quizApi.updateQuizApiV1QuizzesUpdatePut
operation_ids = set()
for route in router.routes:
    # Ensure operation id is unique
    number_of_operation_ids = len(operation_ids)
    operation_ids.add(str(route.name))
    if number_of_operation_ids == len(operation_ids):
        print(operation_ids)
        raise KeyError(
            f"Each api endpoint must have a unique name. "
            f"{route.name} is used as the name of multiple endpoints. "
            f"Change the endpoint's name to fix this error."
        )
    route.operation_id = route.name
