from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.core import DateField, FloatField
from app import db

class SignUpForm(Form):
    '''Form fields with validation for user sign up.'''
    
    firstname = StringField("First Name", [validators.Length(min=1, max=50)], id='firstname', render_kw={'minlength': 1, 'maxlength': 50, 'required': True})
    lastname = StringField("Last Name", [validators.Length(min=1, max=50)], id='lastname', render_kw={'minlength': 1, 'maxlength': 50, 'required': True })
    biography = StringField("Biography", [validators.Length(max=100)], id='biography', render_kw={'maxlength': 100})
    phone = StringField("Phone", [validators.Length(min=9, max=10)], id='phone', render_kw={'minlength': 9, 'maxlength': 10, 'required': True})
    username = StringField("Username", [validators.Length(min=4, max=30)], id='username', render_kw={'minlength': 4, 'maxlength': 30, 'required': True})
    email = StringField("Email", [validators.Length(min=6, max=50)], id='email', render_kw={'minlength': 6, 'maxlength': 50, 'required': True})
    password = PasswordField(
        "Password", 
        [ 
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords do not match."),
            validators.Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]", 
                flags=0, 
                message="Must contain at least one uppercase, lowercase, special character, and number."
            ),
            validators.Length(min=8, max=128)
        ],
        id='password',
        render_kw={'minlength': 8, 'maxlength': 120, 'required': True}
    )
    confirm = PasswordField("Confirm Password", id='confirm')

# EventForm class, Builder Pattern implementation
class EventFormBase(Form):
    # Form fields with validation for event creation.
    title = StringField("Title", [validators.Length(min=1, max=50)])
    date = StringField("Date", [validators.Length(min=1, max=12)])
    latitude = FloatField("Latitude")
    longitude = FloatField("Longitude")
    # For date: entering a value of 010203 stores it as 2001-02-03

class EventFormFull(EventFormBase):
    # Form fields for all possible fields that we save.
    description = StringField("Description", [validators.Length(min=1, max=500)])
    street = StringField("Street", [validators.Length(min=1, max=100)])
    city = StringField("City", [validators.Length(min=1, max=50)])
    state = StringField("State", [validators.Length(min=2, max=2)])

# Event class, Builder Pattern implementation
class EventBase(db.Model):

    __tablename__ = "events" # connects to events table in our database.

    # list of required attributes for an event.
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class EventFull(EventBase):
    # full list of details that can be saved into the database
    description = db.Column(db.Text)
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))

class CreatedEvent(db.Model):
    '''Stores the event created and the user id of who created it.'''

    __tablename__ = "created_events"

    id = db.Column(db.Integer, primary_key=True)

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref("created_events")) # many-to-one with users.id
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    event = db.relationship("Event", backref="created_events") # one-to-one with events.id

class Bookmark(db.Model):
    '''Stores the event bookmarked and the user id of who bookmarked it.'''

    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref("bookmarks")) # optional many-to-optional many with users.id
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    event = db.relationship("Event", backref="bookmarks") # one-to-one with events.id

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
    signup_date = db.Column(db.DateTime)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    biography = db.Column(db.String(255))

    # foreign key
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", backref=db.backref("users", uselist=False)) # one-to-one with roles.id
    
db.create_all()