import os
import re
import requests
import json


from flask import Flask, session
from flask import render_template, request
from flask import request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
with app.app_context():
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

engine = create_engine(uri)#os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#with app.app_context():
#    db.create_all()
#Login stuff

#Index html
@app.route("/", methods = ["GET", "POST"])
def index():
    #Search here
    #Login here
    if request.method == "POST":
        #SQL ADD IT
        newusername = request.form.get("newusername")
        newpassword = request.form.get("newpassword")
        #NewUser = User(username = newusername,password = newpassword)
        db.execute("INSERT INTO users (username, password) VALUES (:username,:password)", {"username": newusername, "password": newpassword})
        #db.session.add(NewUser)
        return render_template("index.html")

    if request.method == "GET":
        return render_template("index.html")


    #return render_template("index.html")


#Link to registration
@app.route("/registration")
def registration():
    return render_template("registration.html")

#book page will be general for all books
@app.route("/bookspage")
def bookspage():
    return render_template("bookspage.html")


#search page for displaying the search results
@app.route("/search", methods = ["POST"])
def search():
    username = request.form.get("username")
    password = request.form.get("password")

    return render_template("search.html",username=username, password = password)

@app.route("/searchresults", methods = ["POST"])
def searchresults():
    searchword = request.form.get("searchword")
    res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": searchword, "maxResults": 40,"projection": "lite"})
    bookinfo = res.json()

    results = []
    for i in range(0,len(bookinfo["items"])-1):
        tempbook = bookinfo["items"][i]["volumeInfo"]["title"]#,bookinfo["items"][i]["volumeInfo"]["authors"]]
        results.append(tempbook)


    #return results[0] #bookinfo["items"][0]["volumeInfo"]["title"]
    return render_template("searchresults.html",results = results)

@app.route("/api/<string:isbn>")
def api(isbn):
    res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": f"isbn:{isbn}"})
    bookinfo = res.json()
    bookinfo = (bookinfo["items"][0])
    title = (bookinfo["volumeInfo"]["title"])
    authors = (bookinfo["volumeInfo"]["authors"])
    publishedDate = (bookinfo["volumeInfo"]["publishedDate"])
    ISBN_10 = (bookinfo["volumeInfo"]["industryIdentifiers"][0]["identifier"])
    ISBN_13 = (bookinfo["volumeInfo"]["industryIdentifiers"][1]["identifier"])
    reviewCount = (bookinfo["volumeInfo"]["ratingsCount"])
    averageRating = (bookinfo["volumeInfo"]["averageRating"])

    infor = {"title": title, "authors": authors, "publishedDate": publishedDate, "ISBN_10": ISBN_10, "ISBN_13": ISBN_13,"reviewCount": reviewCount,"averageRating": averageRating}

    return(json.dumps(infor))
    #return isbn
