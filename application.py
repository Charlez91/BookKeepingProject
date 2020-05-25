import os

from flask import Flask, session, render_template, redirect, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wtforms_fields import * #Form

from login import *

DEBUG = True
import psycopg2 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ibryriynppxdtm:1275b6e1b940231cd521c3bbeab604da37c50304f8e429cc1b24fc4f2b3d7f58@ec2-54-225-227-125.compute-1.amazonaws.com:5432/d1brpuvqqbfnk1'
db = SQLAlchemy(app)



API_key = 'HMOBPhAT2PnNTFaV4BiqEw'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))







class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.Required(),
                            validators.EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service</a> and the <a href="/privacy/">Privacy Policy</a>',
                             [validators.Required()])


@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        #check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "This username is taken!"
        #Add user to DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.commit()
        
    return render_template('login.html', form=reg_form)




























#@app.route('/register/', methods=["GET", "POST"])
#def register_page():
#    try:
#        form = RegistrationForm(request.form)

#        if request.method == "POST" and form.validate():
#            username = form.username.data
#            email = form.email.data
#            password = sha256.crypt.encrypt((str(form.password.data)))
#            c, conn = connection()
#            x = c.execute("SELECT * FROM users WHERE username = (%s)",
#                          (thwart(username)))
#            if int(len(x)) > 0:
#                flash("This username is already taken, please choose another")
#                return render_template('register.html', form=form)
#            else:
#                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
#                          (thwart(username), thwart(password), thwart(email), thwart




#@app.route('/')
#def home():
#    """renders a sample page."""
#    return "hello world!"

@app.route('/welcome')
def welcome():
    return render_template('welcome.html') #render template



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)



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
