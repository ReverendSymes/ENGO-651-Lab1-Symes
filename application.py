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
        message = request.form.get("message")


        #NewUser = User(username = newusername,password = newpassword)
        db.execute("INSERT INTO users (username, password) VALUES (:username,:password)", {"username": newusername, "password": newpassword})
        db.commit()
        return render_template("index.html",message = message)

    if request.method == "GET":
        message = "please log in"
        return render_template("index.html", message = message)


#Link to registration
@app.route("/registration")
def registration():
    global message
    message = "Registration success"
    return render_template("registration.html")

#book page will be general for all books
@app.route("/bookspage", methods = ["POST"])
def bookspage():
    global searchpick
    searchpick = request.form.get("searchpick")
    searchpick = id[int(searchpick)]

    res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": searchpick})
    bookinfo = res.json()
    bookinfo = (bookinfo["items"][0])
    title = (bookinfo["volumeInfo"]["title"])
    authors = (bookinfo["volumeInfo"]["authors"])
    publishedDate = (bookinfo["volumeInfo"]["publishedDate"])
    ISBN_10 = (bookinfo["volumeInfo"]["industryIdentifiers"][0]["identifier"])
    ISBN_13 = (bookinfo["volumeInfo"]["industryIdentifiers"][1]["identifier"])
    reviewCount = (bookinfo["volumeInfo"]["ratingsCount"])
    if reviewCount >= 3:
        vibe = "is a good book"
    if reviewCount < 3:
        vibe = "is why we do not trust reviews"
    averageRating = (bookinfo["volumeInfo"]["averageRating"])
    pics = bookinfo["volumeInfo"]["imageLinks"]["thumbnail"]

    #reviewpeeps = db.execute(f"SELECT review FROM gbreviews WHERE (bookid = {searchpick})").fetchall()

    return render_template("bookspage.html",title = title, authors = authors, publishedDate = publishedDate,reviewCount = reviewCount,averageRating = averageRating,vibe=vibe,ISBN_10=ISBN_10,pics = pics)


#search page for displaying the search results
@app.route("/search", methods = ["POST", "GET"])
def search():
    global username
    username = request.form.get("username")
    password = request.form.get("password")
    ressy = db.execute("SELECT username FROM users").fetchall()
    ressy2 = db.execute("SELECT password FROM users").fetchall()
    oktogo = "False"
    message = "login error please try again"
    for i in range(0,len(ressy)-1):
        if str(ressy[i][0]) == str(username):
            for i in range(0,len(ressy2)-1):
                if str(ressy2[i][0]) == str(password):
                    oktogo = "True"
    if oktogo == "True":
        message = "log in success"
        return render_template("search.html",username=username, password = password,ressy=ressy, message = message)

    else:
         return render_template("index.html", message = message )

@app.route("/searchresults", methods = ["POST"])
def searchresults():
    global id
    searchword = request.form.get("searchword")
    res = requests.get("https://www.googleapis.com/books/v1/volumes", params={"q": searchword, "maxResults": 40,"projection": "lite"})
    bookinfo = res.json()

    results = []
    id = []
    for i in range(0,len(bookinfo["items"])-1):
        tempbook = bookinfo["items"][i]["volumeInfo"]["title"]#,bookinfo["items"][i]["volumeInfo"]["authors"]]
        tempid = bookinfo["items"][i]["id"]
        results.append(tempbook)
        id.append(tempid)
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

@app.route("/reviewsubmitted", methods = ["POST"])
def reviewsubmitted():
    reviewtext = request.form.get("reviewtext")
    goosenumber = request.form.get("goosenumber")
    global searchpick

    bookid = searchpick
    global username
    #username = username
    reviewpeeps = db.execute("SELECT username FROM gbreviews").fetchall()
    postit = 1
    for i in range(0,len(reviewpeeps)):
        if reviewpeeps[i][0] == username:
            postit = 2
            message = "you have already reviewed this book"
    if postit == 1:
        db.execute("INSERT INTO gbreviews (bookid, review, username,rating) VALUES (:bookid,:reviewtext,:username,:goosenumber)", {"bookid": bookid, "reviewtext": reviewtext, "username" : username,"goosenumber": goosenumber})
        db.commit()
        message = "review submitted"
    return render_template("success.html",message = message)

@app.route("/logout", methods = ["POST", "GET"])
def logout():
    global username
    global message
    username = None
    message = "Logged out"
    return render_template("index.html",message = message)
