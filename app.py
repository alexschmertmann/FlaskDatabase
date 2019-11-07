from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser,dbpass,dbhost,dbname)
#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']= 'SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class amschmertmann_star_wars(db.Model):
    MovieID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(255))
    ReleaseDate = db.Column(db.Date)
    Episode = db.Column(db.Integer)
    TimeLineOrder = db.Column(db.Integer)

def __repr__(self):
    return "id: {0} | Name: {1} | Release Date: {2} | Episode: {3} | Time Line Order: {4}".format(self.id,self.Name,self,ReleaseDate,self.Episode,self.TimeLineOrder)

class MovieForm(FlaskForm):
    Name = StringField('Name:', validators=[DataRequired()])
    ReleaseDate = StringField('Release Date:', validators=[DataRequired()])
    Episode = StringField('Episode:', validators=[DataRequired()])
    TimeLineOrder = StringField('Time Line Order:', validators=[DataRequired()])

@app.route('/')
def index():
    all_movies = amschmertmann_star_wars.query.all()
    return render_template('index.html', movies = all_movies, pageTitle='Star Wars Films')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = amschmertmann_star_wars(Name=form.Name.data,ReleaseDate=form.ReleaseDate.data,Episode=form.Episode.data,TimeLineOrder=form.TimeLineOrder.data)
        db.session.add(movie)
        db.session.commit()
        return redirect('/')

    return render_template('add_movie.html', form=form, legend="Add a movie", pageTitle ='Add a movie')

@app.route('/movies/<int:MovieID>', methods=['GET','POST'])
def movie(MovieID):
    movie = amschmertmann_star_wars.query.get_or_404(MovieID)
    return render_template('movies.html', form=movie, pageTitle='Movie Details')

@app.route('/movies/<int:MovieID>/update', methods=['GET','POST'])
def update_movie(MovieID):
    movie = amschmertmann_star_wars.query.get_or_404(MovieID)
    form = MovieForm()
    if form.validate_on_submit():
        movie.Name = form.Name.data
        movie.ReleaseDate = form.ReleaseDate.data
        movie.Episode = form.Episode.data
        movie.TimeLineOrder = form.TimeLineOrder.data
        db.session.commit()
        flash('Your movie has been updated.')
        return redirect(url_for('movie', MovieID=movie.MovieID))
    #elif request.method == 'GET':
    form.Name.data = movie.Name
    form.ReleaseDate.data = movie.ReleaseDate
    form.Episode.data = movie.Episode
    form.TimeLineOrder.data = movie.TimeLineOrder
    return render_template('add_movie.html', form=form, pageTitle='Update Post',
                            legend="Update A Movie")

@app.route('/movies/<int:MovieID>/delete', methods=['POST'])
def delete_movie(MovieID):
    if request.method == 'POST': #if it's a POST request, delete the movie from the database
        movie = amschmertmann_star_wars.query.get_or_404(MovieID)
        db.session.delete(movie)
        db.session.commit()
        flash('Movie was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

