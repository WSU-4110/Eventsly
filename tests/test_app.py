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
@patch('app.engine')
@patch('app.sha256_crypt.verify', return_value=True)
@patch('app.session_login')
def test_LoginValid(app,client,session):
    #Mocking database connection, encryption library, session login method
    mock1 = Mock('app.engine')
    mock2 = Mock('app.sha256_crypt.verify', return_value=True)
    mock3 = Mock('app.session_login')

    #assert that POST request to login follows the redirect
    assert client.post('/login.html', data = dict(
        username = "testusername",
        password="Password!1",
    ), follows_redirects=True)
    
    mock1.assert_any_call #assert that the database connection was called
    mock2.assert_any_call #assert that password verification was called
    mock3.assert_any_call #assert that app session was called
    mock3.assert_called_once #assert that login method was called once

def test_LoginInvalid(app,client,session):
    #Mock database connection, encryption library, session login method
    mock1 = Mock('app.engine')
    mock2 = Mock('app.sha256_crypt.verify', return_value=False)
    mock3 = Mock('app.session_login')
    
    #assert that invalid login doesn't follow redirect
    assert client.post('/login.html', data = dict(
        username = "testusername",
        password="Password!1",
    ))

    mock1.assert_any_call #assert database connection was used
    mock2.assert_any_call #assert password verification was called
    mock3.assert_not_called #assert that session login method was not called


#endregion

#Logout Test
@patch('app.is_logged_in', return_value=True)
@patch('app.session_clear')
def test_Logout(app,client):
    #Mock login verification and session clear methods
    mock1 = Mock('app.is_logged_in')
    mock2 = Mock('app.session_clear')

    assert client.get('/logout', follows_redirects=True) #assert logout method redirects

    mock1.assert_called_once #assert login verification method called once
    mock2.assert_called_once #assert session clear method called once

#Dashboard Test
@patch('app.engine')
@patch('app.is_logged_in')
def test_Dashboard(app,client):
    #Mock database connection and login verification method
    mock1 = Mock('app.engine')
    mock2 = Mock('app.is_logged_in')

    res = client.get('/dashboard.html')
    
    mock1.assert_any_call #assert database connection used to get user events
    mock2.assert_called_once #assert login verification is called once

#Delete Event Test
@patch('app.is_logged_in')
@patch('app.engine')
def test_DeleteEvent(app,client):
    #Mock database connection and login verification method
    mock1 = Mock('app.engine')
    mock2 = Mock('app.is_logged_in')

    assert client.post('/deleteEvent', follows_redirects=True) #assert deleteEvent POST request follows redirect

    mock1.assert_any_call #assert database connection is used to delete event info
    mock2.assert_called_once #assert login verification is called once

#Delete Account Test
@patch('app.is_logged_in')
@patch('app.engine')
def test_DeleteAccount(app,client):
    #Mock database connection and login verification method
    mock1 = Mock('app.engine')
    mock2 = Mock('app.is_logged_in')
    mock3 = Mock('app.session_clear')

    assert client.post('/deleteAccount',follows_redirects=True) #assert POST request to deleteAccount follows redirect
    
    mock1.assert_any_call #assert database connection is used to delete account invo
    mock2.assert_called_once #assert login verification is called once
    mock3.assert_called_once #assert session clear method is called