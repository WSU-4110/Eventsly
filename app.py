from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'splite:///apple.db' # the name is random. if you can think of a better one feel free to replace it.
db = SQLAlchemy(app)

class account(db.Model): # Creates a class to hold login information with.
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable = False)
    password = db.Column(db.String(30), nullable = False)

    def __repr__(self): # Function that returns a string everytime a new element is created.
        return '<Element %r>' % self.id

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

if __name__ == "__main__":
    app.run(debug=True)