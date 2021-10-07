from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventsly.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200),nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' %  self.id


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

@app.route("/register.html", methods=['POST'])
def register():
    if request.method == 'POST':
        user_firstname = request.form['firstname']
        user_lastname = request.form['lastname']
        user_phone = request.form['phone']
        user_email = request.form['email']
        user_username = request.form['username']
        user_password = request.form['password']

        new_user = User(firstname = user_firstname, lastname = user_lastname, phone = user_phone,
        email = user_email, username = user_username, password = user_password)
    
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/register.html')
        except:
            return 'Unable to create your account. Please try again later.'
    else:
        return render_template("/register.html")

if __name__ == "__main__":
    app.run(debug=True)