from functools import partial
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


def create_mem_db(metadata, db):
    """Replace the Session with an in-memory SQLite session for testing.

    Flask-SQLAlchemy 3.x: We override the session binding to use an in-memory
    engine. Requires an active Flask app context when called.

    Returns a scoped session bound to the in-memory engine.
    Call db.restore_engine() in tearDown() to clean up.
    """
    engine = create_engine('sqlite:///:memory:',
                           echo=False,
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    metadata.create_all(engine)

    def _restore_engine(self):
        db.session.remove()
        del self.restore_engine
        del self._test_engine

    db._test_engine = engine
    db.restore_engine = partial(_restore_engine, db)

    # Remove existing session and reconfigure to use the in-memory engine
    db.session.remove()
    db.session.configure(bind=engine)

    return db.session
