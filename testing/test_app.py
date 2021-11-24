from unittest import mock
from flask import session
from unittest.mock import MagicMock, Mock, patch
import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import false, select, true
from werkzeug.wrappers import request
from passlib.hash import sha256_crypt
import logger
import models
from app import fromForm, search
import requests
import pytest

# tests for home() /////
def test_home(client):
    homepage = client.get('/')
    assert homepage.status_code == 302 # redirects to index.html

# /////////////////////

# tests for index() /////
def test_index(client):
    homepage = client.get("/index.html")
    assert homepage.status_code == 200 # asserts we find the correct page

# /////////////////////

# tests for aboutus() /////
def test_aboutus(client):
    page = client.get("/aboutus.html")
    assert client.get("/aboutus/").data == page.data # asserts the page is displaying intended data

# /////////////////////

# tests for search() /////
def test_search(app, client):
    mock1 = Mock('app.engine')
    page = client.get("/search.html")
    assert page.status_code == 200 # asserts we find the correct page
    mock1.assert_any_call # asserts that a connection is made to the database to search events

# /////////////////////

# tests for fromForm() /////
def test_fromForm(app, client):
    mock1 = Mock('app.engine')
    with pytest.raises(RuntimeError) as excinfo:
        fromForm('findEvent')
    assert "Working outside of request context." in str(excinfo.value) # asserts that a request is being made to the form

# /////////////////////

# tests for createEvent() /////
def test_createEvent(client):
    mock1 = Mock('app.engine')
    page = client.get("/createEvent.html")
    assert page.status_code == 302 # asserts we find the correct page
    mock1.assert_any_call # asserts that a connection is made to the database to add an event

# /////////////////////