import os

from flask import Flask, session, render_template, redirect, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_wtf import Form, FlaskForm
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, SubmitField, validators, StringField #Form
from login import *
from login import User
from login import db
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
import psycopg2
from psycopg2 import connect
DEBUG = True
FLASK_DEBUG=1


app = Flask(__name__)
app.secret_key = 'replace later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xkirkgsdjndrtd:04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d64djukmaep4ov'
db = SQLAlchemy(app)
app.debug = True


API_key = 'HMOBPhAT2PnNTFaV4BiqEw'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))

def invalid_credentials(form, field):
    """Username and password checker"""
    username_entered = form.username.data
    password_entered = field.data

    # Check if credentials is valid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("One of the details is incorrect")

    elif password_entered != user_object.password:
        raise ValidationError("One of the details is incorrect")




class RegistrationForm(Form):

    username = StringField('Username', validators=[InputRequired(message="Username required"), Length(min=4, max=20,
                                                                               message="Username between 4 and 25 characters")])
    email = TextField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', validators=[InputRequired(message="Use required"), Length(min=4, max=20,
                                                                               message="Username between 4 and 25 characters")])
    confirm = PasswordField('Repeat Password', validators=[InputRequired(message="Password required"),
                                                           EqualTo('password', message="Passwords must match")])
    #accept_tos = BooleanField('I accept the <a href="/tos/">Terms of
    #Service</a> and the <a href="/privacy/">Privacy Policy</a>',
                             #[validators.Required()])

    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists, please use a different username")
    
    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()
        if user_object:
            raise ValidationError("Email already exists, please use a different email")

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    # updates database on successful registration
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        email = reg_form.email.data

        #adding user to DB
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()            

        return redirect(url_for('signin'))
    return render_template('login.html', form=reg_form)


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('username', validators=[InputRequired(message="Username Required")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Create')

@app.route('/signin', methods=['GET', 'POST'])
def signin():

    login_form = LoginForm()
    
    # Allow login if validation success
    if login_form.validate_on_submit():
        return "Successfully logged in"

    return render_template('sign_in.html', form=login_form)





















#@app.route("/add")
#def add_book():
#    name=request.args.get('name')
#    author=request.arg.get('author')
#    published=request.args.get('published')
#    try:
#        book=Book(
#            name=name,
#            author=author,
#            published=published
#        )
#        db.session.add(book)
#        db.session.commit()
#        return "Book added. book id={}".format(book.id)
#    except Exception as e:
#        return(str(e))



if __name__ == '__main__':
  
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=Tr)
