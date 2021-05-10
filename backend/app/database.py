from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import settings

# # Logic to log to a file
# import logging
# log_file_name = "db.log"
# handler_level = logging.INFO
# logger_level = logging.INFO
#
# handler = logging.FileHandler(log_file_name)
# handler.setLevel(handler_level)
#
# logger = logging.getLogger("sqlalchemy")
# logger.addHandler(handler)
# logger.setLevel(logger_level)

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    future=True,
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
