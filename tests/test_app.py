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

#Create Event (Needed to Test Bookmarks)
@patch('app.is_logged_in')
@patch('app.engine')
def test_createEvent(app, client, session):
    res = client.post('/createEvent.html', data=dict(
        title = "Test",
        description = "Descript",
        date = "11/30/21",
        latitude = "50.534333",
        longitude = "10.343445",
        street = "Sycamore",
        city = "Detroit",
        state = "MI"
    ))

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