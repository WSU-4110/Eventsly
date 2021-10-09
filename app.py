from flask import Flask, render_template, request, redirect, flash, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from datetime import datetime

app = Flask(__name__)

#Configurate MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kiddobean19'
app.config['MYSQL_DB'] = 'eventsly'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#initialize MYSQL
mysql = MySQL(app)

class RegisterForm(Form):
    firstname = StringField('Firstname', [validators.Length(min = 1, max=50)])
    lastname = StringField('Lastname', [validators.Length(min = 1, max=50)])    
    phone = StringField('Phone', [validators.Length(min=9,max=10)])
    username = StringField('Username', [validators.Length(min=4, max=30)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password.')

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
        firstname = form.firstname.data
        lastname = form.lastname.data
        phone = form.phone.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data)) #encrypt password

        #Create cursor
        cur = mysql.connection.cursor() #used to execute commands

        cur.execute("INSERT INTO users(firstname, lastname, phone, email, username, password) VALUES(%s, %s, %s, %s, %s, %s )", 
        (firstname, lastname, phone, email, username, password))

        #commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('Your account has been created!', 'success')
        redirect(url_for('index.html'))
    return render_template("register.html", form=form)
    


if __name__ == "__main__":
    app.run(debug=True)