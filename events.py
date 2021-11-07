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
from app import app, db, engine, is_logged_in
import models

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

@app.route("/createEvent.html", methods=['POST','GET'])
@is_logged_in
def createEvent():
    form = models.EventForm(request.form)
    if request.method == 'POST' and form.validate():

        new_event = models.Event(
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

                    #After inserting event, get event id and add to created_events table
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