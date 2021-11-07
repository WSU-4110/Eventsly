from datetime import datetime
from functools import wraps
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select
from flask import Flask, render_template, request, redirect, flash, url_for, session
from passlib.hash import sha256_crypt
import sqlalchemy
import traceback
import logger
from app import app, db, engine, is_logged_in
import models

@app.route("/bookmarks.html")
@is_logged_in
def bookmarks():
    with engine.begin() as conn:
        query = sqlalchemy.text(f'SELECT * FROM events, bookmarks WHERE bookmarks.user_id = {session["userid"]} AND events.id = bookmarks.event_id ORDER BY bookmarks.id')
        rows = conn.execute(query)
        bookmarkpull = rows.mappings().all()

    return render_template("bookmarks.html", title="Bookmarks", bookmarkpull=bookmarkpull)