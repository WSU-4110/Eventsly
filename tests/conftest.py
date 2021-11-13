from flask import sessions
import pytest
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from app import app as flask_app
from app import db as _db
from app import session, logger

@pytest.fixture(autouse=True)
def app(request):
    flask_app.config.from_object('config.TestingConfig')
    flask_app.logger.info(f"DBURI: {flask_app.config['SQLALCHEMY_DATABASE_URI']}")
    engine = create_engine(flask_app.config['SQLALCHEMY_DATABASE_URI'],echo=True, future=True)

    yield flask_app

    dropQueries = [sqlalchemy.text(f"DROP TABLE IF EXISTS users CASCADE"), sqlalchemy.text(f"DROP TABLE IF EXISTS events CASCADE"), sqlalchemy.text(f"DROP TABLE IF EXISTS created_events CASCADE"), sqlalchemy.text(f"DROP TABLE IF EXISTS bookmarks CASCADE"), sqlalchemy.text(f"DROP TABLE IF EXISTS roles CASCADE")]
    with engine.begin() as conn:
        for query in dropQueries:
            conn.execute(query)


@pytest.fixture(autouse=True)
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def db(app, request):
    with app.app_context():
        _db.create_all()
        yield _db

        _db.drop_all

@pytest.fixture(scope="function")
def session(app, db, request):

    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)

    _db.session=session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()