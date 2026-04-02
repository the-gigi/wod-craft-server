from functools import partial
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


def create_mem_db(metadata, db):
    """Replace the Session class with an in-memory test Session class

    In Flask-SQLAlchemy 3.x, we override the engine by configuring the app
    with an in-memory SQLite URI. This function sets up the tables and
    returns a scoped session bound to the in-memory engine.
    """
    engine = create_engine('sqlite:///:memory:',
                           echo=False,
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    metadata.create_all(engine)

    # Store original engine-providing mechanism
    original_engine = db.engine

    def _restore_engine(self):
        # Re-bind the session to the original engine
        db.session.remove()
        delattr(self, 'restore_engine')
        delattr(self, '_test_engine')

    db._test_engine = engine
    db.restore_engine = partial(_restore_engine, db)

    # Override the session to use the in-memory engine
    db.session.remove()
    db.session.configure(bind=engine)

    return db.session
