from flask import session
import sqlalchemy
from sqlalchemy.sql.expression import select
from werkzeug.wrappers import request
import logger
import models

def test_HomeRedirectsToIndex(app,client):
    res = client.get('/')
    assert res.status_code ==302 #assert redirect to index

#region SignUp Tests
def test_SignUpIsFound(app,client):
    res=client.get('/signup.html')
    assert res.status_code == 200

def test_SignUpValid(app,client,session):
    app.logger.info(app)
    res = client.post('/signup.html', data=dict(
        firstname="Test",
        lastname="User",
        phone="0000000000",
        email="testuseremail@test.com",
        username="testusername",
        password="Password!1",
        confirm="Password!1"
    ))
    
    result = [r for r in session.query(models.User)][0]

    assert result.username == "testusername"
    assert result.email == "testuseremail@test.com"
    assert res.status_code == 302

def test_SignUpInvalidPassword(app,client):
    res = client.post('/signup.html', data=dict(
        firstname="Test",
        lastname="User",
        phone="0000000000",
        email="testuseremail@test.com",
        username="testusername",
        password="invalid",
        confirm ="invalid"
    ))
    
    assert res.status_code == 400
    
#endregion

#region Login Tests
# def test_LoginValid(app,client):
#     res = client.post('/login.html', data = dict(

#     ))
#endregion