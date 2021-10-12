from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/createAccount.html")
def createAccount():
    return render_template("createAccount.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/createEvent.html")
def login():
    return render_template("createEvent.html")

if __name__ == "__main__":
    app.run(debug=True)