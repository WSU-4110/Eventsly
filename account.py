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


@app.route('/logout')
@is_logged_in #uses is_logged_in wrapper for this URL
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard.html')
@is_logged_in
def dashboard():
    with engine.begin() as conn:
        query = sqlalchemy.text(f'SELECT * FROM events, created_events WHERE created_events.user_id = {session["userid"]} AND events.id = created_events.event_id ORDER BY created_events.id')
        rows = conn.execute(query)
        myEvents = rows.mappings().all()

    app.logger.info(f'User events: {myEvents}')
    return render_template('dashboard.html', title="Dashboard", myEvents=myEvents)