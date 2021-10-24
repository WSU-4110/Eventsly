from datetime import datetime
from logging import error
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, select
from flask import Flask, render_template, request, redirect, flash, sessions, url_for, session, logging
from passlib.hash import sha256_crypt
from sqlalchemy.util.langhelpers import NoneType
import logger
import traceback
import os

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

@app.route("/")
def home():
    return render_template("index.html", title="Eventsly")

@app.route("/index.html")
def index():
    return render_template("index.html", title="Eventsly")

@app.route("/bookmarks.html")
def bookmarks():
    return render_template("Bookmarks.html", title="Bookmarks")

@app.route("/about.html")
def about():
    return render_template("About.html", title="About Us")

@app.route("/contact.html")
def contact():
    return render_template("Contact.html", title="Contact")

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
        stmt = select(models.User.username, models.User.password).where(models.User.username == username_input)
        with engine.connect() as conn:
            result = conn.execute(stmt).first()

        app.logger.info(f'Query result: {result}')
        app.logger.info(f'SELECT user query executed.\n Query: {stmt}')

        if result != None:
            #Get stored hash
            password_data = result.password
        
            #Compare passwords
            if sha256_crypt.verify(password_input, password_data):
                session['Logged_in'] = True
                session['username'] = username_input

                flash('You are now logged in', 'success')
                app.logger.info('Password input matched password stored in database')
                return redirect(url_for('index.html'))
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
def logout():
    session.clear()
    flash('You are now logged out')
    return redirect(url_for('index.html'))
    
@app.route("/createEvent.html")
def createEvent():
    return render_template("createEvent.html", title="Create Event")

if __name__ == "__main__":
    app.secret_key='wsu4110eventsly'
      
    app.logger.info(app.config)
    app.run(debug=True)
