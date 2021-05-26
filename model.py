#from app import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20),primary_key=True,unique=True)
    password = db.Column(db.String(30),unique=True)
    email = db.Column(db.String(20),unique=True)
    number = db.Column(db.String(20),unique=True)
    Fname = db.Column(db.String(20), nullable=True)
    Lname = db.Column(db.String(20), nullable=True)
    courses = db.relationship('Courses',backref='course',lazy=True)
    SIC = db.relationship('StudentsInCourses',backref='sic',lazy=True)
    type = db.Column(db.Integer(),nullable=True)
    #SIC = db.relationship('StudentsInCourses',backref='sic',lazy=True)


class Courses(db.Model):
    #id = db.Column(db.Integer(),primary_key=True)
    CourseName = db.Column(db.String(40),primary_key=True)
    Iusername = db.Column(db.String(20),db.ForeignKey('user.username'))
    courname = db.relationship('StudentsInCourses',backref='courssename',lazy=True)

class StudentsInCourses(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    coursename =  db.Column(db.String(40),db.ForeignKey('courses.CourseName'))
    #Iusername = db.Column(db.String(20),db.ForeignKey('courses.Iusername'))
    Susername = db.Column(db.String(20),db.ForeignKey('user.username'))

def get_id(self):
    """Return the email address to satisfy Flask-Login's requirements."""
    return self.username
