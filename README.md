# Eventsly

## What is Eventsly?

###### Eventsly is the one-stop solution to finding events in your area. Simply open the web application, search your location, and go. 
###### Events in your area will be shown and you can feel free to coordinate your own events, all for others to find places to be, and the hot spots around their area. 
###### Concerts, games, get-togethers, you name it! It can be done with Eventsly.

## Group Members

- Greg Flores
- Devin Stawicki
- Racquel Martens
- Mark Slattery
- CJ Fox

## Running the Eventsly Application Locally

1. run the command `git clone https://github.com/WSU-4110/Eventsly` in a bash terminal to clone the Eventsly repo
2. install Postgresql from https://www.postgresql.org/download/
3. Set up Postgresql with default settings (Postgresql Stack Builder is not necessary)
4. launch pgAdmin4 and create a database on the server named `eventsly`
5. take note of the password you set for the database, create a file named 'dbconfig.txt' in the Eventsly repo with the only line in that file being the password you set
6. install virtualenv `pip install virtualenv`
7. install the other dependencies by navigating to the Eventsly repo top level in a bash terminal and running the command `pip install -r requirements.txt`
8. add a new environment variable to your system's environment variables: variable name: `FLASK_ENV` value: `development`
###### At this point, your environment is set up to run the application locally - the following commands describe what you should do each coding session
7. navigate to the Eventsly repo top level in a bash terminal and run the command `source env/Scripts/activate` to create a virtual environment
8. run the command `flask run` to launch the app on localhost


## Technology Stack

### Front end
---
- HTML
- CSS
- Javascript

### Back end
---
- Python (Flask)
- PostgreSQL Database

### Hosting Service (Deployment)
---
- Heroku
