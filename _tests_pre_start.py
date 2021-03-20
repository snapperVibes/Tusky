import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core import settings
from app import crud
from app.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def wait_for_database_to_be_setup() -> None:
    try:
        db = SessionLocal()
        crud.user.get_by_name_and_number(db, name=settings.FIRST_SUPERUSER, number=0)
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    logger.info("Initializing service")
    wait_for_database_to_be_setup()
    logger.info("Service finished initializing")
