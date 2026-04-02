from functools import partial


def create_mem_db(metadata, db):
    """Set up (or reset) in-memory SQLite database for testing.

    The app must have been created with testing=True (SQLALCHEMY_DATABASE_URI = 'sqlite://').
    This function drops all tables and recreates them, giving a clean slate.

    Returns the current db.session.
    """
    with db.engine.begin() as conn:
        metadata.drop_all(conn)
        metadata.create_all(conn)

    db.session.remove()

    def _restore_engine(self):
        """Called in tearDown - drops all test tables."""
        with db.engine.begin() as conn:
            metadata.drop_all(conn)
        db.session.remove()

    db.restore_engine = partial(_restore_engine, db)

    return db.session
