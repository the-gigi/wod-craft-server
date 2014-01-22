from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_mem_db(metadata):
    """Replace the Session class with an in-memory test Session class

    Very useful for fast and non-destructive tests (avoid hitting real DB)
    """
    engine = create_engine('sqlite:///:memory:', echo=False)
    metadata.create_all(engine)

    return sessionmaker(bind=engine)()

