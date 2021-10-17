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

class EventForm(Form):
    title = StringField('Title')
    description = StringField('Description')
    address = StringField('Address')
    latitude = StringField('Latitude')
    longitude = StringField('Longitude')
    date = StringField('Date')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(50))
    address = db.Column(db.String(50))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    date = db.Column(db.Integer)

db.create_all()