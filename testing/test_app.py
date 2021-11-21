from datetime import datetime
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


#region SignUp Tests
def test_SignUpIsFound(app,client):
    res=client.get('/signup.html')
    assert res.status_code == 200 #assert OK HTTP status code

# tests for home() /////
def test_home(client):
    homepage = client.get('/')
    assert homepage.status_code == 302

# /////////////////////

# tests for index() /////
def test_index(client):
    homepage = client.get("/index.html")
    assert homepage.status_code == 200

# /////////////////////

# tests for aboutus() /////
def test_aboutus(client):
    page = client.get("/aboutus.html")
    assert client.get("/aboutus/").data == page.data

# /////////////////////

# tests for search() /////
def test_search(client):
    page = client.get("/search.html")
    assert page.status_code == 200

# /////////////////////

# tests for createEvent() /////
def test_createEvent(client):
    page = client.get("/createEvent.html")
    assert page.status_code == 302

# /////////////////////