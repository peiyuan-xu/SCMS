# Using init db, this function will create tables automatically.

from scms.db import common
from scms.db.models import ModelBase


def init_db():
    ModelBase.metadata.create_all(common.get_engine())


if __name__ == "__main__":
    init_db()
