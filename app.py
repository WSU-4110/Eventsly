from datetime import datetime
from functools import wraps
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select
from flask import Flask, render_template, request, redirect, flash, url_for, session
from passlib.hash import sha256_crypt
import sqlalchemy
import traceback

app = Flask(__name__)

if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
if app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
    app.logger.info(f'{app.config}')
else:
    app.config.from_object('config.BaseConfig')

db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],echo=True, future=True)

import models

#Check if user logged in to access logout and dashboard
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login.','danger')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
def home():
    return redirect(url_for('index'))

@app.route("/index.html")
def index():
    pins = []
    with engine.begin() as conn:
        query = sqlalchemy.text('SELECT * FROM events WHERE date > CURRENT_TIMESTAMP')
        rows = conn.execute(query)
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

@app.route("/bookmarks.html")
@is_logged_in
def bookmarks():
    with engine.begin() as conn:
        query = sqlalchemy.text(f'SELECT * FROM events, bookmarks WHERE bookmarks.user_id = {session["userid"]} AND events.id = bookmarks.event_id ORDER BY bookmarks.id')
        rows = conn.execute(query)
        bookmarkpull = rows.mappings().all()

    return render_template("bookmarks.html", title="Bookmarks", bookmarkpull=bookmarkpull)

@app.route("/about.html")
def about():
    return render_template("About.html", title="About Us")

@app.route("/search.html", methods =['GET','POST'])
def search():
    hereValue = 'default value'
    if request.method == 'POST':
        # Get data from form
        hereValue = request.form['findEvent']

    with engine.begin() as conn:
        query = sqlalchemy.text("SELECT * FROM events WHERE title LIKE '%" + hereValue + "%'")
        rows = conn.execute(query)
        hereData = rows.mappings().all()

    app.logger.info(f"data is {hereData}")
    
    return render_template("search.html", title="Find Events", data = hereData)

@app.route("/signup.html", methods=['POST','GET'])
def signup():
    form = models.SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        encryptpassword = sha256_crypt.encrypt(str(form.password.data)) #encrypt password

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
            return redirect(url_for('signup'))

    return render_template("signup.html", form=form, title="Sign Up")

@app.route("/login.html", methods =['GET','POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        username_input = request.form['username']
        password_input = request.form['password']

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
                session['logged_in'] = True
                session['username'] = result.username
                session['userid'] = result.id
                session['name'] = f'{result.firstname} {result.lastname}'

                flash('You are now logged in', 'success')
                app.logger.info('Password input matched password stored in database')
                return redirect(url_for('dashboard'))
            else:
                app.logger.info('Password input did not match password stored in database')
                error = 'Invalid login'
                return render_template('login.html', title = 'Log In',error=error)
        else:
            app.logger.info('No user found with that username')  
            error = 'Username not found'
            return render_template('login.html', title = 'Log In', error=error)

    return render_template("login.html", title="Log In")

@app.route("/createEvent.html", methods=['POST','GET'])
@is_logged_in
def createEvent():
    form = models.EventFormFull(request.form)
    if request.method == 'POST' and form.validate():

        new_event = models.EventFull(
            title = form.title.data, 
            description = form.description.data,
            date = form.date.data, 
            latitude = form.latitude.data, 
            longitude = form.longitude.data,
            street = form.street.data,
            city = form.city.data,
            state = form.state.data,
        )
        try:
            db.session.add(new_event)
            db.session.commit()
            app.logger.info(f'Event {form.title.data} was created.')
            flash('Your event has been created!', 'success')
            return redirect(url_for('index'))
        except:
            flash('Unable to make your event','failure')
            # print call stack
            app.logger.warning(traceback.format_exc())
            app.logger.warning(f"Event {form.title.data} was unable to be created. /////")
            return redirect(url_for('createEvent'))
    return render_template("createEvent.html",form = form, title="Create Event")

@app.route('/logout')
@is_logged_in #uses is_logged_in wrapper for this URL
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard.html')
@is_logged_in
def dashboard():
    return render_template('dashboard.html', title="Dashboard")



if __name__ == "__main__":
    app.secret_key='wsu4110eventsly'
      
    app.run()
