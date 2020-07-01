import os

from flask import Flask, flash, session, render_template, redirect, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_wtf import Form, FlaskForm
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, SubmitField, validators, StringField #Form
from login import *
from login import User
from login import db
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
import psycopg2
from psycopg2 import connect
import pprint
import requests
#from elasticsearch import Elasticsearch
from search import Post, Books
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "HMOBPhAT2PnNTFaV4BiqEw", "isbns": "9781632168146"})
print(res.json())
DEBUG = True
FLASK_DEBUG=1


app = Flask(__name__)
app.secret_key = 'replace later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xkirkgsdjndrtd:04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d64djukmaep4ov'
SQLALCHEMY_TRACK_MODIFICATIONS = True
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
#engine = create_engine(os.getenv("postgres://xkirkgsdjndrtd:04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d64djukmaep4ov"))
engine = create_engine("postgres://xkirkgsdjndrtd:04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d64djukmaep4ov")
db = scoped_session(sessionmaker(bind=engine))

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
    password = PasswordField('Password', validators=[InputRequired(message="Password required"), Length(min=4, max=20,
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
        db.add(user)
        db.commit()            

        return redirect(url_for('signin'))
    return render_template('login.html', form=reg_form)


class LoginForm(FlaskForm):
    """Login form"""
    
    username = StringField('username', validators=[InputRequired(message="Username Required")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    flash("welcome!")
    login_form = LoginForm()
    
    # Allow login if validation success
    if login_form.validate_on_submit():
        return redirect('/search') #we will redirect to search

    return render_template('sign_in.html', form=login_form)



#class SearchForm(FlaskForm):
#    search = StringField('search')
#    submit_button = SubmitField('Search')

@app.route('/search', methods=['GET', 'POST'])
def search_page():
        
    return render_template("search.html")

@app.route('/results', methods=['POST'])
def search_results():
    if request.method == 'POST':
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        year = request.form.get("year")
        author = request.form.get("author")

        #session = Session()
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        results = db.query(Books).all()
        #if results==None:
        #    flash("No books found")

        #    return render_template("search.html")
        
        for result in results:
            if (title in result.title) is True:

                list1.append(result.isbn)
                list2.append(result.title)
                list3.append(result.author)
                list4.append(result.year)
        #if (title in result.title) is False:
        #    flash("Book not Found!")
            

        lister = []
        lister.append(list1), lister.append(list2), lister.append(list3), lister.append(list4)
        if (lister[1]==[]):
            flash("Book not Found!")
        return render_template("results.html", count=len(list1), result1=lister)

                








if __name__ == '__main__':
  
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=Tr)
