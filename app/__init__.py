# Avoid circular imports by importing models AFTER Base
# Importing app.models adds the models to the base
from app.database import Base
import app.models


def initdb(**kw):
    pass


def dropdb(**kw):
    pass
