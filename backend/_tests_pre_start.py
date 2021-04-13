import logging

# tenacity is a library to retry code until it succeeds
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core import settings
from app import crud
from app.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 15
wait_seconds = 1

from time import sleep

sleep(2)


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def wait_for_database_to_be_setup() -> None:
    try:
        db = SessionLocal()
        admin = crud.user.get_by_name(
            db,
            name=settings.FIRST_SUPERUSER,
            number=0,
        )
        if err := admin.err():
            raise err
        return
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    logger.info("Initializing service")
    wait_for_database_to_be_setup()
    logger.info("Service finished initializing")
