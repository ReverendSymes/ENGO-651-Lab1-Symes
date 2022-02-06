#Python script to import books.csv to my heroku DATABASE

#import the stuff
import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#Pull up db from  DATABASE_URL

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

engine = create_engine(uri)#os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

book = open("books.csv")
book = csv.reader(book)

for isbn, title, author, year in book:
    db.execute("INSERT INTO importbooks (isbn, title, Author, year) VALUES (:isbn, :title, :Author, :year)"{"isbn": isbn, "title": title, "author": author, "year": year }")

db.commit()
