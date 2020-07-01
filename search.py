from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, SelectField
from flask_sqlalchemy import Model
#from flask_migrate import Migrate


app =  Flask(__name__)
db = SQLAlchemy(app)


#app = Flask(__name__)

#app.config[SQLALCHEMY_DATABASE_URI] = 'postgres://xkirkgsdjndrtd:04923e2fd7f601d40372a5aaef449d4b76fd601fd6171926c73b5421bc9ce23b@ec2-34-225-82-212.compute-1.amazonaws.com:5432/d64djukmaep4ov'

class Post(Form):

    choices = [('isbn', 'isbn'),
               ('title', 'title'),
               ('author', 'author')]

    select = SelectField('Search for book:', choices=choices)
    search=StringField('')
     
class Books(db.Model):
    __tablename__ = "books"

    isbn = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.Text)
    author = db.Column(db.Text)
    year = db.Column(db.String(50))
#if __name__ == '__main__':
#    app.run(debug=True)
