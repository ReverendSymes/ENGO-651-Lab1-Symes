from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ ="users"
    username = db.Column(db.String, primary_key = True)#nullable = False)
    password = db.Column(db.String,nullable = False)
