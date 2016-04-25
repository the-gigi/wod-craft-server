from flask.ext.script import Manager, prompt_bool
from sqlalchemy import create_engine
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
def create():
    """Creates database tables from sqlalchemy models"""
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    metadata.create_all(engine)


@db_manager.command
def recreate(default_data=True, sample_data=False):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()
    create(default_data, sample_data)


manager = Manager(app)
manager.add_command('db', db_manager)

if __name__ == "__main__":
    manager.run()
