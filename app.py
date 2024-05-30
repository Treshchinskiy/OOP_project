from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import CheckConstraint

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ILIFIA80'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1474747vd@localhost/Rec_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)



class Comment(db.Model):
    __tablename__='comment'
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    stars = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    
    __table_args__ = (
        CheckConstraint('stars >= 1 AND stars <= 5', name='stars_range'),
    )
 


class Movies(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    genres = db.Column(db.String(500), nullable=False)  #JSON 
    keywords = db.Column(db.String(500), nullable=False)  #JSON
    overview = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    runtime = db.Column(db.Float, nullable=True)
    title = db.Column(db.String(200), nullable=False)
    vote_average = db.Column(db.Float, nullable=False)
    cast = db.Column(db.String(1000), nullable=False)  #JSON 
    crew = db.Column(db.String(1000), nullable=False)  #JSON 
    
    def __repr__(self):
        return f'<Movie {self.title}>'
    




