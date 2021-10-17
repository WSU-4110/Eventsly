from flask import Flask, render_template, request, redirect, flash, sessions, url_for, session, logging
from passlib.hash import sha256_crypt
from logger import *
import os

app = Flask(__name__)
from models import *

if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
elif app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
else:
    app.config.from_object('config.BaseConfig')
    
app.logger.info(app.config)

@app.route("/")
def home():
    return render_template("index.html", title="Eventsly", pageStyles="main {padding: 0;}")

@app.route("/index.html")
def index():
    return render_template("index.html", title="Eventsly", pageStyles="main {padding: 0;}")

@app.route("/Bookmarks.html")
def bookmarks():
    return render_template("Bookmarks.html", title="Bookmarks")

@app.route("/About.html")
def about():
    return render_template("About.html", title="About Us")

@app.route("/Contact.html")
def contact():
    return render_template("Contact.html", title="Contact")

@app.route("/register.html", methods=['POST','GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        encryptpassword = sha256_crypt.encrypt(str(form.password.data)) #encrypt password

        new_user = Users(firstname = form.firstname.data,lastname = form.lastname.data, phone = form.phone.data, 
        email = form.email.data, username = form.username.data, password = encryptpassword)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            app.logger.info(f'User {form.username.data} account was created.')
            flash('Your account has been created!', 'success')
            return redirect(url_for('index'))
        except:
            flash('Unable to make your account','failure')
            app.logger.warning(f"User {form.username.data} account was unable to be created. Username or email already in use.")
            return redirect(url_for('register'))


    return render_template("register.html", form=form, title="Register")

@app.route("/login.html")
def login():
    return render_template("login.html", title="Log In")

@app.route("/createEvent.html")
def createEvent():
    return render_template("createEvent.html", title="Create Event")

if __name__ == "__main__":
    app.secret_key='wsu4110eventsly'
    app.run(debug=True)
