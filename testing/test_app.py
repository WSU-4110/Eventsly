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