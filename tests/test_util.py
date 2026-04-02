from functools import partial
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


def create_mem_db(metadata, db):
    """Set up in-memory SQLite database for testing with Flask-SQLAlchemy 3.x.

    This approach creates an in-memory SQLite engine and binds the Flask-SQLAlchemy
    session to it directly, bypassing the configured database URI.

    The app must be configured with SQLALCHEMY_DATABASE_URI = 'sqlite://' for this
    to work correctly.
    """
    # Create tables in the existing in-memory engine  
    with db.engine.begin() as conn:
        metadata.create_all(conn)

    def _restore_engine(self):
        # Drop all tables to clean up
        with db.engine.begin() as conn:
            metadata.drop_all(conn)

    db.restore_engine = partial(_restore_engine, db)

    return db.session
