from datetime import datetime
from logging import error
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, flash, url_for, session, logging
from passlib.hash import sha256_crypt
import logger
import traceback
import os

app = Flask(__name__)

if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
elif app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
else:
    app.config.from_object('config.BaseConfig')

db = SQLAlchemy(app)

import models

@app.route("/")
def home():
    return render_template("index.html", title="Eventsly", pageStyles="main {padding: 0;}")

@app.route("/index.html")
def index():
    return render_template("index.html", title="Eventsly", pageStyles="main {padding: 0;}")

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
            app.logger.info(f'User {form.username.data} account was created.')
            flash('Your account has been created!', 'success')
            return redirect(url_for('index'))
        except:
            flash('Unable to make your account','failure')
            # print call stack
            app.logger.warning(traceback.format_exc())
            # app.logger.warning(f"User {form.username.data} account was unable to be created. Username or email already in use.")
            return redirect(url_for('signup'))

    return render_template("signup.html", form=form, title="Sign Up")

@app.route("/login.html")
def login():
    return render_template("login.html", title="Log In")

@app.route("/createEvent.html")
def createEvent():
    return render_template("createEvent.html", title="Create Event")

if __name__ == "__main__":
    app.secret_key='wsu4110eventsly'
      
    app.logger.info(app.config)
    app.run(debug=True)
