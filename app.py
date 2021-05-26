import flask_login
from flask import Flask,render_template, redirect, url_for , request, session, flash
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from model import db, User   #, Courses, StudentsInCourses
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,validators
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
import bcrypt
import os
import cv2


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://algorithm:root@localhost/education'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
#db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    number = StringField('number', validators=[InputRequired()])



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        #global name
        session['username'] = form.username.data


        #return '<h1>Invalid username or password</h1>'
        #return '<h1>' + name + ' ' + form.password.data + '</h1>'
        return render_template('InstructorHomepage.html', name=session['username'])

    return render_template('login.html', form=form)
















@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, number=form.number.data)
        #name = request.form['name']
        #email = request.form['email']
        #password = request.form['password'].encode('utf-8')
        #number = request.form['number']
        #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        #getUserData(new_user)

        #new_user = User(username=name, email=email, password=hash_password, number=number)
        db.session.add(new_user)
        db.session.commit()

        #return '<h1>New user has been created!</h1>'
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)


@app.route('/profile')
@login_required
def dashboard():
    return render_template('InstructorHomepage.html', name=session['username'])





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def cambtn():
    #name = form.username.data
    #print(UserMixin.current_user.username)
    filename = 'video_'+session['username']+'.avi'
    #print(session['username'])
    #filename = 'video.avi'
    #print(filename)
    frames_per_second = 24.0
    res = '720p'

    # Set resolution for the video capture
    # Function adapted from https://kirr.co/0l6qmh
    def change_res(cap, width, height):
        cap.set(3, width)
        cap.set(4, height)

    # Standard Video Dimensions Sizes
    STD_DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }

    # grab resolution dimensions and set video capture to it.
    def get_dims(cap, res='1080p'):
        width, height = STD_DIMENSIONS["480p"]
        if res in STD_DIMENSIONS:
            width, height = STD_DIMENSIONS[res]
        ## change the current caputre device
        ## to the resulting resolution
        change_res(cap, width, height)
        return width, height

    # Video Encoding, might require additional installs
    # Types of Codes: http://www.fourcc.org/codecs.php
    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']

    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))



    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return render_template('profile_test.html')

    cap.release()
    out.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    app.run()

