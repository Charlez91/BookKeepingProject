import os
import sys

from flask import Flask, flash, session, render_template, redirect, url_for, request, current_app, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_wtf import Form, FlaskForm
from wtforms import TextField, BooleanField, PasswordField, SubmitField, validators, StringField, TextAreaField, RadioField
from wtforms.validators import InputRequired, Length, EqualTo, Email, ValidationError, DataRequired
import psycopg2
from psycopg2 import connect
import pprint
import requests
from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy
from models import User, Books, Reviews
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import simplejson as json

res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "HMOBPhAT2PnNTFaV4BiqEw", "isbns": "9781632168146"})

DEBUG = True
FLASK_DEBUG=1


app = Flask(__name__)
app.secret_key = 'replace later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xkirkgsdjndrtd:04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d64djukmaep4ov'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = False
db = SQLAlchemy(app)
app.debug = True
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Bootstrap(app)
API_key = 'HMOBPhAT2PnNTFaV4BiqEw'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Set up database
#engine = create_engine(os.getenv("postgres://xkirkgsdjndrtd:04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d64djukmaep4ov"))
engine = create_engine("postgres://xkirkgsdjndrtd:04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d64djukmaep4ov")
Session = scoped_session(sessionmaker(bind=engine))
session = Session()


def invalid_credentials(form, field):
    """Username and password checker"""
    username_entered = form.username.data
    password_entered = field.password.data

    # Check if credentials is valid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("One of the details is incorrect")
       

    elif password_entered != user_object.password:
        raise ValidationError("One of the details is incorrect")


class RegistrationForm(FlaskForm):

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
        hashed_password = generate_password_hash(reg_form.password.data, method='sha256')
        username = reg_form.username.data
        password = hashed_password
        email = reg_form.email.data

        #adding user to DB
        user = User(username=username, password=password, email=email)
        session.add(user)
        session.commit()            

        return redirect(url_for('login'))
    return render_template('login.html', form=reg_form)


@login_manager.user_loader
def user_loader(id):
    """Given *user_id*, return the associated Userobject"""
    #the current user is current_user.username remember this later while working with id
    return User.query.get(int(id))


class LoginForm(FlaskForm):
    """Login form"""
    
    username = StringField('username', validators=[InputRequired(message="Username Required")])
    password = PasswordField('password', validators=[InputRequired(message="Password required")])
    submit_button = SubmitField('Login')


@app.route('/signin', methods=['GET', 'POST'])
def login():
    # to prevent a logged in user from logging in again:
    if current_user.is_authenticated:
        return redirect(url_for('search_page'))
    form = LoginForm()
    
    # Allow login if validation success
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('search_page')) #we will redirect to search
        flash('Invalid credentials')
        return redirect(url_for('login'))

    return render_template('sign_in.html', form=form)


@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search_page():
        
    return render_template("search.html")

@app.route('/results', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        #retrieve input from form
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        year = request.form.get("year")
        author = request.form.get("author")

        
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        list5 = []

        results = Books.query.all()
        
        for result in results:
            if (title in result.title) is True:

        # the result.id will attach to each book at every iteration
                list1.append(result.isbn)
                list2.append(result.title)
                list3.append(result.author)
                list4.append(result.year)
                list5.append(result.id)
           

        lister = []
        lister.append(list1), lister.append(list2), lister.append(list3), lister.append(list4), lister.append(list5)

        if (lister[1]==[]):
            flash("Book not Found!")
        
        return render_template("results.html", count=len(list1), result1=lister)

class SubmitReview(FlaskForm):

    comment = TextAreaField("what do you think about this book?", validators=[DataRequired("required")])
    rating = RadioField('How would you rate this book?', choices=[(1, 'bad: 1'), (2, 'fair: 2'), 
                                                                    (3, 'good: 3'), (4, 'very good: 4'), 
                                                                    (5, 'excellent: 5')], default=None, coerce=int)
    submit = SubmitField('submit')


def fetch_user_comment(users_id, books_id):
    reviews = Reviews.query.filter_by(users_id=users_id).filter_by(books_id=books_id)
    
    return reviews

@app.route('/404_page', methods=['POST', 'GET'])
def error_page():
    return render_template('404.html')

@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book_details(id):
    
    book = Books.query.get(id)
    page_id = book.id
    page_isbn = book.isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "HMOBPhAT2PnNTFaV4BiqEw", "isbns":page_isbn.strip()})
    
    if res.status_code == 200:
        data = res.json()
        print(data.keys())
        for k in data['books']:
                goodreads_rating = k['average_rating']
                ratings_count = k['ratings_count']
    else:
        goodreads_rating = "Not available"
        ratings_count = "Not available"

    form = SubmitReview()
    book_reviews = book.reviews
    func = fetch_user_comment

    if (current_user.id in [b.users.id for b in book_reviews]) is False:
        if form.validate_on_submit():
            comment = form.comment.data
            rating = int(form.rating.data)
            review = Reviews(books_id=page_id, comment=comment, 
                                users_id=current_user.id, rating=rating)
            session.add(review)
            session.commit()
            return "succesful"
        else:
            flash("one of the fields is empty")
    else:
        flash("you already made a comment")
  
    rating_list = []
    for b in book_reviews:
        rating_list.append(b.rating)
    if len(rating_list) == 0:
        ave_rating = "no rating yet"
    else:
        ave_rating = sum(rating_list)/len(rating_list)
    no_of_comments = len(rating_list)

    my_api = [{'title': book.title}, {'author': book.author }, {'year': book.year}, 
              {'isbn': page_isbn}, {'review_count': no_of_comments}, {'average_score': ave_rating}]
    
    print(my_api)

    return render_template('reviews.html', book_details=book_details,
                            func=func, book_reviews=book_reviews, book=book,
                           form=form, page_id=page_id, ave_rating=ave_rating, 
                           goodreads_rating=goodreads_rating, ratings_count=ratings_count)

@app.route('/api/', methods=["GET"])
def get_all_api():
    books = Books.query.all()

    output = []
    
    for book in books:
        rating_list = []
        book_data = {}
        book_data['isbn'] = book.isbn.strip()
        book_data['title'] = book.title
        book_data['author'] = book.author
        book_data['year'] = book.year
        book_review = book.reviews
        for b in book_review:
            rating_list.append(b.rating)
        if len(rating_list) == 0:
            ave_rating = "no rating yet"
        else:
            ave_rating = sum(rating_list)/len(rating_list)
        book_data['review_count'] = len(rating_list)
        book_data['average_score'] = ave_rating

        output.append(book_data)

    return jsonify({'books' : output})

@app.route('/api/<string:isbn>', methods=['GET'])
def get_api(isbn):
    book = Books.query.filter_by(isbn=isbn).first()

    if book==None:
        return redirect(url_for('error_page'))

    book_reviews = book.reviews
    rating_list = []
   
    for b in book_reviews:
        rating_list.append(b.rating)
    if len(rating_list) == 0:
        ave_rating = "no rating yet"
    else:
        ave_rating = round(sum(rating_list)/len(rating_list), 2)
    no_of_comments = len(rating_list)

    my_api = [{'title': book.title}, {'author': book.author }, {'year': book.year}, 
              {'isbn': isbn}, {'review_count': no_of_comments}, {'average_score': ave_rating}]
    
    return jsonify({'my_api' : my_api})




if __name__ == '__main__':
  
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)