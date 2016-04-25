from flask.ext.script import Manager, prompt_bool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import wodcraft.api.models as am
from wodcraft.api.models import metadata
from wodcraft.api.api import create_app

app = create_app()
db = app.db


db_manager = Manager(usage="Perform database operations")


@db_manager.command
def drop():
    """Drop database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@db_manager.command
@db_manager.option('-p', dest='populate')
def create(populate=False):
    """Creates database tables from sqlalchemy models"""
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    metadata.create_all(engine)
    if populate:
        Session = sessionmaker(bind=engine)
        session = Session()
        _populate(session)

@db_manager.command
def recreate(populate=False):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()
    create(populate)


def _populate(session):
    """Add some test data"""
    # Add admin and regular users
    user = am.User()
    user.name = 'the_gigi'
    user.email = 'the_gigi@gmail.com'
    user.role = am.ROLE_ADMIN
    session.add(user)

    user2 = am.User()
    user2.name = 'nobody'
    user2.email = 'nobody@aol.com'
    user2.role = am.ROLE_USER
    session.add(user2)

    # Add a few activities
    activities = []
    for i in range(3):
        a = am.Activity()
        a.name = 'activity_{}'.format(i)
        activities.append(a)
        session.add(a)

    # Add a few tags
    tags = []
    for k in range(2):
        t = am.Tag()
        t.user = user
        t.tag = 'tag_{0}'.format(k)
        tags.append(t)
        session.add(t)

    # Add a few scores + tags
    for i in range(3):
        for j in range(2):
            s = am.Score()
            s.user = user
            s.activity = activities[i]
            s.rx = j == 0
            s.reps = j
            for k in range(j + 1):
                s.tags.append(tags[k])
            session.add(s)
    session.commit()





manager = Manager(app)
manager.add_command('db', db_manager)

if __name__ == "__main__":
    manager.run()
