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
    assert res.status_code == 200 #assert OK HTTP status code

def test_SignUpValid(app,client,session):
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

    assert result.username == "testusername" #assert actual equals expected username
    assert result.email == "testuseremail@test.com" #assert actual equals expected email
    assert res.status_code == 302 #assert that it follows redirect

def test_SignUpInvalidPassword(app,client, session):
    res = client.post('/signup.html', data=dict(
        firstname="Test",
        lastname="User",
        phone="0000000000",
        email="testuseremail@test.com",
        username="testusername",
        password="invalid",
        confirm ="invalid"
    ))

    result = [r for r in session.query(models.User)]
    assert len(result) == 0 #assert list from query is empty
    assert res.status_code == 400 #assert BAD REQUEST
    
#endregion

#region Login Tests
# def test_LoginValid(app,client):
#     res = client.post('/login.html', data = dict(

#     ))
#endregion