from unittest import mock
from flask import sessions
import pytest
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from app import app as flask_app
from app import db as _db
from app import session, logger

@mock.patch('requests.get', mock.Mock(side_effect = lambda k:{search.hereData: 'Event 12'}.get(k, 'unhandled request %s'%k)))

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

@pytest.fixture
def requests_mock():
    #request.form('POST', 'findEvent', text='Success')
    resp = request.form['findEvent']
    resp.text

@pytest.fixture
def mock_event1():
    event1 = Event(
        title="Event 12",
        description="This is event number 12.",
        date="2022-01-02",
        state="mi",
        city="City 1",
        street="Street 1",
        latitude="42.355744",
        longitude="-83.068577"
    )
    return event1

@pytest.fixture
def mock_event2():
    event2 = Event(
        title="$Event!",
        description="This is event number 2.",
        date="2022-01-07",
        state="mi",
        city="City2 &",
        street="Street 2!",
        latitude="42.355744",
        longitude="-83.068577"
    )
    return event2

@pytest.fixture
def mock_event3():
    event3 = Event(
        title="Event #3",
        description="This is event number 3.",
        date="2022-01-12",
        state="mi",
        city="City -3",
        street="Street 3.",
        latitude="42.355744",
        longitude="-83.068577"
    )
    return event3