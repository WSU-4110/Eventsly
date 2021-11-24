import pytest
from datetime import datetime
from typing import ByteString
from unittest import mock
from flask import session
from unittest.mock import MagicMock, Mock, patch
import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import false, select, true
from werkzeug.wrappers import request
from passlib.hash import sha256_crypt
from app import fromForm
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
"""
This file (test_app.py) contains the unit tests for the app.py file bookmarks functionality.
"""

#Bookmark Route Test
@patch('app.is_logged_in')
@patch('app.engine')
def test_bookmarks(app, client):
    mock1 = Mock('app.engine')
    mock2 = Mock('app.is_logged_in')

    res = client.get('/bookmarks.html')

    mock1.assert_any_call #assert database connection used to get user events
    mock2.assert_called_once #assert login verification is called once

#Bookmark Add Test
@patch('app.is_logged_in')
@patch('app.engine')
def test_addBookmark(app, client, session):
    res = client.post('/bookmarks.html', data=dict(
        user_id = 1,
        event_id = 1,
    ))

    result = [r for r in session.query(models.User)]
    assert len(result) == 0 #assert list from query is empty


    mock1 = Mock('app.engine')
    mock2 = Mock('app.is_logged_in')
                    
    assert client.post('/addBookmark', follows_redirects=True) #assert addBookmark POST request follows redirect

    mock1.assert_any_call #assert database connection is used to delete account invo
    mock2.assert_called_once #assert login verification is called once

#Bookmark Delete Test
@patch('app.is_logged_in')
@patch('app.engine')
def test_deleteBookmark(app, client):
    mock1 = Mock('app.engine')
    mock2 = Mock('app.is_logged_in')
                    
    assert client.post('/deleteBookmark', follows_redirects=True) #assert addBookmark POST request follows redirect

    mock1.assert_any_call #assert database connection is used to delete account invo
    mock2.assert_called_once #assert login verification is called once

#Failed Bookmark Addition Test
@patch('app.is_logged_in')
@patch('app.engine')
def test_failedBookmark(app, client):
    with app.test_client() as c:
        res = c.get('/addBookmark/2')
        assert client.post('/addBookmark/2', follows_redirects=True)

#Failed Bookmark Deletion Test
@patch('app.is_logged_in')
@patch('app.engine')
def test_failedDeletion(app, client):
    with app.test_client() as c:
        res = c.get('/deleteBookmark/2')
        assert client.post('/deleteBookmark/2', follows_redirects=True)

#Bookmark Route Failed Test
@patch('app.is_logged_in')
@patch('app.engine')
def test_bookmarkRouteFail(app, client):
    mock1 = Mock('app.engine')
    mock2 = Mock('app.is_logged_in')

    res = client.get('/bookmark.html')

    mock1.assert_any_call #assert database connection used to get user events
    mock2.assert_called_once #assert login verification is called once

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
@patch('app.engine')
def test_fromForm(app, client):
    mock1 = Mock('app.engine')
    with pytest.raises(RuntimeError) as excinfo:
        fromForm('findEvent')
    assert "Working outside of request context." in str(excinfo.value) # asserts that a request is being made to the form

# /////////////////////

# tests for createEvent() /////
@patch('app.engine')
def test_createEvent(client):
    mock1 = Mock('app.engine')
    page = client.get("/createEvent.html")
    assert client.get("/createEvent.html", follows_redirects=True)
    mock1.assert_any_call # asserts that a connection is made to the database to add an event

# /////////////////////
