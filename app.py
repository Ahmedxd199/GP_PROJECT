from flask import Flask,render_template, redirect, url_for , request,session
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from model import db, User   #, Courses, StudentsInCourses
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
import bcrypt



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

        #return '<h1>Invalid username or password</h1>'
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

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

        #new_user = User(username=name, email=email, password=hash_password, number=number)
        db.session.add(new_user)
        db.session.commit()

        #return '<h1>New user has been created!</h1>'
        return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))





if __name__ == '__main__':
    app.run()

