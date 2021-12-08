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

#region App Initialization
app = Flask(__name__)

if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig') # pragma: no cover
if app.config['ENV'] == 'development' and app.config['TESTING'] == False:
    app.config.from_object('config.DevelopmentConfig')
else:
    app.config.from_object('config.BaseConfig')

db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],echo=True, future=True)
import models   

#Helpers
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login.','danger')
            return redirect(url_for('login'))
    app.logger.info(f"WRAP: {wrap}")
    return wrap

def session_clear():
    session.clear()

def session_login(user):
    session['logged_in'] = True
    session['username'] = user.username
    session['userid'] = user.id
    session['name'] = f'{user.firstname} {user.lastname}'

#endregion

#region Basic Functionalities
@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/index.html")
def index():
    pins = []
    with engine.begin() as conn:
        queryGetPins = sqlalchemy.text('SELECT * FROM events WHERE date > CURRENT_TIMESTAMP')
        rows = conn.execute(queryGetPins)
        for row in rows:
            pin = {
                "id": row.id,
                "latitude" : row.latitude,
                "longitude" : row.longitude,
                "date": row.date,
                "street" : row.street,
                "city" : row.city,
                "state" : row.state,
                "title" : row.title,
                "description" : row.description
            }
            pins.append(pin)
    return render_template("index.html", title="Eventsly", pins=pins)

@app.route("/about.html")
def about():
    return render_template("About.html", title="About Us",code=200)
#endregion

#region Account Functionalities
@app.route("/signup.html", methods=['POST','GET'])
def signup():
    form = models.SignUpForm(request.form)

    app.logger.info(request.form)
    app.logger.info(form.firstname.data)
    app.logger.info(form.password.data)
    app.logger.info(f'valid? :{form.validate()}')
    if request.method == 'POST' and form.validate():
        encryptpassword = sha256_crypt.hash(str(form.password.data)) #encrypt password

        new_user = models.User(
            firstname=form.firstname.data, 
            lastname=form.lastname.data, 
            phone=form.phone.data, 
            email = form.email.data, 
            username = form.username.data,
            biography = form.biography.data,
            password = encryptpassword,
            signup_date = datetime.now(),
        )
        app.logger.info
        try:
            db.session.add(new_user)
            db.session.commit()
            app.logger.info(f'User {form.username.data} account was created.')
            flash('Your account has been created!', 'success')
            return redirect(url_for('index'))
        except:
            flash('Unable to make your account','failure')
            # print call stack
            app.logger.warning(traceback.format_exc())
            app.logger.warning(f"User {form.username.data} account was unable to be created. Username or email already in use.")
            return redirect(url_for('signup'), 302)
    if request.method == 'POST' and not form.validate():
        return render_template("signup.html", form=form, title="Sign Up"), 400
    return render_template("signup.html", form=form, title="Sign Up"), 200

@app.route("/login.html", methods =['GET','POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        username_input = request.form['username']
        password_input = request.form['password']

        app.logger.info(f"USERNAME INPUT: {username_input}")

        #Get user by username
        stmt = select(models.User).where(models.User.username == username_input)
        with engine.connect() as conn:
            result = conn.execute(stmt).first()

        app.logger.info(f'Query result: {result}')
        app.logger.info(f'SELECT user query executed.\n Query: {stmt}')

        if result != None:
            #Get stored hash
            password_data = result.password
        
            #Compare passwords
            if sha256_crypt.verify(password_input, password_data):
                session_login(result)

                flash('You are now logged in', 'success')
                app.logger.info('Password input matched password stored in database')
                return redirect(url_for('dashboard'), code = 302)
            else:
                app.logger.info('Password input did not match password stored in database')
                error = 'Invalid login'
                return render_template('login.html', title = 'Log In',error=error)
        else:
            app.logger.info('No user found with that username')  
            error = 'Username not found'
            return render_template('login.html', title = 'Log In', error=error)

    return render_template("login.html", title="Log In")


@app.route('/logout')
@is_logged_in #uses is_logged_in wrapper for this URL
def logout():
    session_clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'), code=302)

@app.route('/dashboard.html')
@is_logged_in
def dashboard():
    with engine.begin() as conn:
        queryGetMyEvents = sqlalchemy.text(f'SELECT * FROM events, created_events WHERE created_events.user_id = {session["userid"]} AND events.id = created_events.event_id ORDER BY created_events.id')
        rows = conn.execute(queryGetMyEvents)
        myEvents = rows.mappings().all()

    app.logger.info(f'User events: {myEvents}')
    return render_template('dashboard.html', title="Dashboard", myEvents=myEvents)

@app.route('/deleteAccount')
@is_logged_in
def deleteAccount():
    with engine.begin() as conn:
        queryGetEvents = sqlalchemy.text(f'SELECT event_id FROM created_events WHERE created_events.user_id= {session["userid"]}')
        rows = conn.execute(queryGetEvents)
        queryDeleteFromCreatedEvents = sqlalchemy.text(f'DELETE FROM created_events WHERE created_events.user_id = {session["userid"]}')
        conn.execute(queryDeleteFromCreatedEvents)
        for row in rows:
            queryDeleteFromEvents = sqlalchemy.text(f'DELETE FROM events WHERE events.id = {row.event_id}')
            queryDeleteEventsFromBookmarks = sqlalchemy.text(f'DELETE FROM bookmarks where bookmarks.event_id = {row.event_id}')
            conn.execute(queryDeleteFromEvents)
            conn.execute(queryDeleteEventsFromBookmarks)
            app.logger.info(f'Deleted event with ID: {row.event_id}')
        queryDeleteBookmarks = sqlalchemy.text(f'DELETE FROM bookmarks where bookmarks.user_id = {session["userid"]}')
        queryDeleteEventsFromBookmarks = sqlalchemy.text(f'DELETE FROM bookmarks where')
        queryDeleteUser= sqlalchemy.text(f'DELETE FROM users WHERE users.id = {session["userid"]}')
        conn.execute(queryDeleteBookmarks)
        conn.execute(queryDeleteUser)
    
    session_clear()
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/deleteEvent/<int:id>', methods = ['POST','GET'])
@is_logged_in
def deleteEvent(id):
    app.logger.warning(f'Deleting event with event ID: {id}')
    eventid = id
    with engine.begin() as conn:
       queryDeleteEventFromCreatedEvents = sqlalchemy.text(f'DELETE FROM created_events where created_events.event_id = {eventid}')
       queryDeleteEventFromBookmarks = sqlalchemy.text(f'DELETE FROM bookmarks WHERE bookmarks.event_id = {eventid}')
       queryDeleteEventFromEvents = sqlalchemy.text(f'DELETE FROM events WHERE events.id = {eventid}')
       conn.execute(queryDeleteEventFromCreatedEvents)
       conn.execute(queryDeleteEventFromBookmarks)
       conn.execute(queryDeleteEventFromEvents)

    flash('Event deleted.', 'success')
    return redirect(url_for('dashboard'))
#endregion

#region Bookmark Functionalities
@app.route("/bookmarks.html")
@is_logged_in
def bookmarks():
    with engine.begin() as conn:
        queryGetBookmarks = sqlalchemy.text(f'SELECT * FROM events, bookmarks WHERE bookmarks.user_id = {session["userid"]} AND events.id = bookmarks.event_id AND date > CURRENT_TIMESTAMP ORDER BY bookmarks.id')
        rows = conn.execute(queryGetBookmarks)
        bookmarkpull = rows.mappings().all()
        app.logger.info(f"Bookmarkpull: {bookmarkpull}")

    return render_template("bookmarks.html", title="Bookmarks", bookmarkpull=bookmarkpull)

@app.route('/addBookmark/<int:id>', methods=['POST', 'GET'])
@is_logged_in
def addBookmark(id):
    with engine.begin() as conn:
        query = sqlalchemy.text(f'SELECT COUNT(*) FROM bookmarks, events WHERE bookmarks.user_id = {session["userid"]} AND bookmarks.event_id = events.id AND CURRENT_TIMESTAMP < events.date')
        result = conn.execute(query).first()[0]
        app.logger.info(f"RESULT: {result}")
        
        if (result >= 15):
            # print call stack
            app.logger.warning(traceback.format_exc())
            flash('Unable to bookmark your event. You have hit the bookmark limit.','failure')
        else:
            with engine.begin() as conn:   
                queryExists = sqlalchemy.text(f'SELECT COUNT(*) FROM bookmarks, events WHERE bookmarks.user_id = {session["userid"]} AND bookmarks.event_id = {id}')
                resultCount = conn.execute(queryExists).first()[0]
                app.logger.info(f"RESULT COUNT: {resultCount}")
                if (resultCount != 0):
                    # print call stack
                    app.logger.warning(traceback.format_exc())
                    flash('Unable to bookmark your event. You have already bookmarked this.','failure')
                else:
                    with engine.begin() as conn:
                        queryInsert = sqlalchemy.text(f'INSERT INTO bookmarks (user_id, event_id) VALUES({session["userid"]}, {id})')
                        resultInsert = conn.execute(queryInsert)
                        app.logger.info(f'Bookmarked: {resultInsert}')
                    flash('Event bookmarked!', 'success')
                    

    return redirect(url_for('index'))


@app.route('/deleteBookmark/<int:id>', methods = ['POST','GET'])
@is_logged_in
def deleteBookmark(id):
    with engine.begin() as conn:
        queryDeleteEventFromBookmarks = sqlalchemy.text(f'DELETE FROM bookmarks WHERE bookmarks.event_id = {id} AND user_id = {session["userid"]}')
        result = conn.execute(queryDeleteEventFromBookmarks)
        app.logger.info(f'Bookmark Deleted: {result}')
    
    flash('Bookmark Removed!', 'success')
    return redirect(url_for('index'))
#endregion

#region Event Functionalities
@app.route("/search.html", methods =['GET','POST'])
def search():
    hereValue = 'default value'
    if request.method == 'POST':
        # Get data from form
        hereValue = request.form['findEvent']

    with engine.begin() as conn:
        querySearchTitle = sqlalchemy.text("SELECT * FROM events WHERE title LIKE '%" + hereValue + "%' and events.date > CURRENT_TIMESTAMP")
        rows = conn.execute(querySearchTitle)
        hereData = rows.mappings().all()

    app.logger.info(f"data is {hereData}")
    
    return render_template("search.html", title="Find Events", data = hereData)

@app.route("/search.html", methods =['GET','POST'])
def fromForm(nameOfField):
    # Get data from form
    hereValue = request.form[nameOfField]
    return hereValue


@app.route("/createEvent.html", methods=['POST','GET'])
@is_logged_in
def createEvent():
    with engine.begin() as conn:
        queryGetMyEvents = sqlalchemy.text(f'SELECT COUNT (*) FROM events, created_events WHERE created_events.user_id = {session["userid"]} AND events.id = created_events.event_id AND CURRENT_TIMESTAMP < events.date')
        result = conn.execute(queryGetMyEvents).first()[0]
        app.logger.info(f'events this user has created: {result}')
    
    form = models.EventForm(request.form)
    if request.method == 'POST' and form.validate():

        new_event = models.Event(
            title = form.title.data, 
            description = form.description.data,
            date = form.date.data, 
            latitude = float(form.latitude.data), 
            longitude = float(form.longitude.data),
            street = form.street.data,
            city = form.city.data,
            state = form.state.data,
        )
        if (result >= 15):
            
            # print call stack
            app.logger.warning(traceback.format_exc())
            app.logger.warning(f"Event {form.title.data} was unable to be created. /////")
            flash('Unable to make your event. You have hit the event creation limit.','failure')
            return redirect(url_for('createEvent'))
        else:
            try:
                db.session.add(new_event)
                db.session.commit()
                app.logger.info(f'Event {form.title.data} was created.')

                # After inserting event, get event id and add to created_events table
                stmt = select(models.Event).order_by(models.Event.id.desc())
                with engine.begin() as conn:
                    result = conn.execute(stmt).first()
                    
                app.logger.info(f"Most recent event: {result}")

                newCreatedEvent = models.CreatedEvent(
                    event_id = result.id,
                    user_id = session['userid']
                )

                db.session.add(newCreatedEvent)
                db.session.commit()
                app.logger.info(f"New Created Event: {newCreatedEvent}")

                flash('Your event has been created!', 'success')
                return redirect(url_for('index'))
            except:
                flash('Unable to make your event','failure')
                # print call stack
                app.logger.warning(traceback.format_exc())
                app.logger.warning(f"Event {form.title.data} was unable to be created. /////")
                return redirect(url_for('createEvent'))
            
    return render_template("createEvent.html",form = form, title="Create Event")

@app.route('/event-details/<eventid>', methods=['POST','GET'])
def eventDetails(eventid):  
    pin = []
    createdEvent=[]
    event={}
    with engine.begin() as conn:
        query = sqlalchemy.text(f'SELECT * from events WHERE id={eventid}')
        result = conn.execute(query)
        for row in result:
            event = {
                "id": row.id,
                "latitude" : row.latitude,
                "longitude" : row.longitude,
                "date": row.date,
                "street" : row.street,
                "city" : row.city,
                "state" : row.state,
                "title" : row.title,
                "description" : row.description
            }
            pin.append(event)

        query2 = sqlalchemy.text(f"SELECT * FROM created_events WHERE created_events.event_id = {eventid}")
        createdEventResult= conn.execute(query2).mappings().all()
        for row in createdEventResult:
            createdEvent = {
                "id" : row.id,
                "user_id": row.user_id,
                "event_id": row.event_id
            }
            
    return render_template('event-details.html', title="Event Details", event=event, pin=pin, createdEvent=createdEvent, code=200)


@app.route('/edit-event/<int:eventid>', methods=['POST','GET'])
@is_logged_in
def editEvent(eventid):
    form = models.EventForm(request.form)
    with engine.begin() as conn:
        queryGetEvent = sqlalchemy.text(f"SELECT * FROM events WHERE events.id = {eventid}")
        result = conn.execute(queryGetEvent)
        for row in result:
            event = {
                "id": row.id,
                "latitude" : row.latitude,
                "longitude" : row.longitude,
                "date": row.date,
                "street" : row.street,
                "city" : row.city,
                "state" : row.state,
                "title" : row.title,
                "description" : row.description
            }

    if request.method == 'POST':
        event_update = models.Event(
            title = form.title.data,
            description = form.description.data,
            date = form.date.data,
            street = form.street.data,
            city = form.city.data,
            state = form.state.data
        )

        with engine.begin() as conn:
            queryUpdateEvent = sqlalchemy.text(f"UPDATE events SET title='{event_update.title}', description='{event_update.description}', date='{event_update.date}', street='{event_update.street}', city='{event_update.city}', state='{event_update.state}' WHERE id = {event['id']}")
            conn.execute(queryUpdateEvent)
        return redirect(url_for('index'))

    return render_template('edit-event.html', event=event, form=form)
#endregion
