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

@app.route("/about.html")
def about():
    return render_template("About.html", title="About Us")

if __name__ == "__main__":
    app.secret_key='wsu4110eventsly'
      
    app.run()
