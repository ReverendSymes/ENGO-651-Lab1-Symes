import os
import re


from flask import Flask, session
from flask import render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

engine = create_engine(uri)#os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#Login stuff

#Index html
@app.route("/")
def index():
    #Search here
    #Login here
    return render_template("index.html")

#Link to registration
@app.route("/registration")
def registration():
    return render_template("registration.html")

#book page will be general for all books
@app.route("/bookspage")
def bookspage():
    return render_template("bookspage.html")

#search page for displaying the search results
@app.route("/searchs", methods = ["POST"])
def searchs():
    #username = request.form.get(username)
    #password = request.form.get(password)

    return render_template("search.html")
