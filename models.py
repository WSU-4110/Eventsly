from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, validators
from app import app

db = SQLAlchemy(app)

class RegisterForm(Form):
    firstname = StringField('Firstname', [validators.Length(min = 1, max=50)])
    lastname = StringField('Lastname', [validators.Length(min = 1, max=50)])    
    phone = StringField('Phone', [validators.Length(min=9,max=10)])
    username = StringField('Username', [validators.Length(min=4, max=30)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match.'),
        validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]", flags=0, 
        message='Password must contain at least one uppercase, lowercase, special character, and number.'),
        validators.Length(min=8)
    ])
    confirm = PasswordField('Confirm Password.')

class Events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    title = db.Column(db.String(100))

class CreatedEvents(db.Model):
    __tablename__ = 'created_events'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey(Events.id))
    event = db.relationship('events', backref='created_events', lazy=True)

class Bookmarks(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey(Events.id))
    event = db.relationship('events', backref='bookmarks', lazy=True)

class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    create_event_self = db.Column(db.Boolean)
    delete_event_self = db.Column(db.Boolean)
    delete_event_other = db.Column(db.Boolean)
    create_account = db.Column(db.Boolean)
    delete_account_self = db.Column(db.Boolean)
    delete_account_other = db.Column(db.Boolean)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    register_date = db.Column(db.DateTime)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    biography = db.Column(db.String(255))

    # Foreign Keys: uselist=False indicates 1-to-1 relationship
    created_events_id = db.Column(db.Integer, db.ForeignKey(CreatedEvents.id))
    created_events = db.relationship('created_events', backref='users', lazy=True, uselist=False)
    bookmarks_id = db.Column(db.Integer, db.ForeignKey(Bookmarks.id))
    bookmarks = db.relationship('bookmarks', backref='users', lazy=True, uselist=False)
    role_id = db.Column(db.Integer, db.ForeignKey(Roles.id))
    role = db.relationship('roles', backref='users', lazy=True, uselist=False)

db.create_all()