from flask import Flask, render_template, request, redirect, flash, url_for, session, logging
from passlib.hash import sha256_crypt
from logger import *

app = Flask(__name__)

from models import *



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/Bookmarks.html")
def bookmarks():
    return render_template("Bookmarks.html")

@app.route("/About.html")
def about():
    return render_template("About.html")

@app.route("/Contact.html")
def contact():
    return render_template("Contact.html")

@app.route("/register.html", methods=['POST','GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        encryptpassword = sha256_crypt.encrypt(str(form.password.data)) #encrypt password

        new_user = User(firstname = form.firstname.data,lastname = form.lastname.data, phone = form.phone.data, 
        email = form.email.data, username = form.username.data, password = encryptpassword)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            app.logger.info(f'User {form.username.data} account was created.')
            flash('Your account has been created!', 'success')
            return redirect(url_for('home'))
        except:
            flash('Unable to make your account','failure')
            app.logger.warning(f"User {form.username.data} account was unable to be created. Username or email already in use.")
            return redirect(url_for('register'))


    return render_template("register.html", form=form)


@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/createEvent.html")
def createEvent():
    return render_template("createEvent.html")


if __name__ == "__main__":
    app.secret_key = 'wsu4110eventsly'
    app.run(debug=True)