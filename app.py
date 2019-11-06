from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser,secrets.dbpass,secrets.dbhost,secrets.dbname)

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
    return "id: {0} | Name: {1} | Realease Date: {2} | Episode: {3} | Time Line Order: {4}".format(self.id,self.Name,self,ReleaseDate,self.Episode,self.TimeLineOrder)

class MovieForm(FlaskForm):
    Name = StringField('Name:', validators=[DataRequired()])
    ReleaseDate = StringField('Realease Date:', validators=[DataRequired()])
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

    return render_template('add_movie.html', form=form, pageTitle ='Add a movie')
if __name__ == '__main__':
    app.run(debug=True)

