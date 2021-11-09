# Installation
Eventsly is a web application, so there is not any installation required to use the app.
The application can be found at https://eventsly.herokuapp.com/

## Running the Eventsly Application Locally

1. Run the command `git clone https://github.com/WSU-4110/Eventsly` in a bash terminal to clone the Eventsly repo
2. Install Postgresql from https://www.postgresql.org/download/
3. Set up Postgresql with default settings (Postgresql Stack Builder is not necessary)
4. Launch pgAdmin4 and create a database on the server named `eventsly`
5. Take note of the password you set for the database, create a file named 'dbconfig.txt' in the Eventsly repo with the only line in that file being the password you set
6. Install virtualenv `pip install virtualenv`
7. Install the other dependencies by navigating to the Eventsly repo top level in a bash terminal and running the command `pip install -r requirements.txt`
8. Add a new environment variable to your system's environment variables: variable name: `FLASK_ENV` value: `development`

**At this point, your environment is set up to run the application locally - the following commands describe what you should do each coding session**
11. navigate to the Eventsly repo top level in a bash terminal and run the command `source env/Scripts/activate` to create a virtual environment
12. run the command `flask run` to launch the app on localhost
