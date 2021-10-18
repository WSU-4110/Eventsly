from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, validators
from app import app

db = SQLAlchemy(app)

class RegisterForm(Form):
    firstname = StringField("Firstname", [validators.Length(min = 1, max=50)])
    lastname = StringField("Lastname", [validators.Length(min = 1, max=50)])
    biography = StringField("Biography", [validators.Length(min=0,max=255)])
    phone = StringField("Phone", [validators.Length(min=9,max=10)])
    username = StringField("Username", [validators.Length(min=4, max=30)])
    email = StringField("Email", [validators.Length(min=6, max=50)])
    password = PasswordField("Password", [
        validators.DataRequired(),
        validators.EqualTo("confirm", message="Passwords do not match."),
        validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]", flags=0, 
        message="Password must contain at least one uppercase, lowercase, special character, and number."),
        validators.Length(min=8)
    ])
    confirm = PasswordField("Confirm Password.")

class Event(db.Model):
    '''Stores all events.'''

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    title = db.Column(db.String(100))

class CreatedEvent(db.Model):
    '''Stores the event created and the user id of who created it.'''

    __tablename__ = "created_events"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("created_events", uselist=False))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    event = db.relationship("Event", backref="created_events")

class Bookmark(db.Model):
    '''Stores the event bookmarked and the user id of who bookmarked it.'''

    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("bookmarks", uselist=False))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    event = db.relationship("Event", backref="bookmarks")

class Role(db.Model):
    '''Stores privileges for account roles.'''

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    create_event_self = db.Column(db.Boolean)
    delete_event_self = db.Column(db.Boolean)
    delete_event_other = db.Column(db.Boolean)
    create_account = db.Column(db.Boolean)
    delete_account_self = db.Column(db.Boolean)
    delete_account_other = db.Column(db.Boolean)

class User(db.Model):
    '''Stores all users.'''

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    register_date = db.Column(db.DateTime)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    biography = db.Column(db.String(255))

    # unsure if necessary
    # created_event_list_id = db.Column(db.Integer, db.ForeignKey("created_events.id"))
    # created_event_list = db.relationship("CreatedEvent", backref=db.backref("users", uselist=False))

    # # One user has one bookmark_list
    # bookmark_list_id = db.Column(db.Integer, db.ForeignKey("bookmarks.id"))
    # bookmark_list = db.relationship("Bookmark", backref=db.backref("users", uselist=False))

    # One user has one role
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", backref=db.backref("users", uselist=False))

db.create_all()