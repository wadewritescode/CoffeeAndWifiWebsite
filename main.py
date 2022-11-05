from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, SelectField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)

COFFEE_CHOICES = [('0', '✘'), ('1', '☕')]
WIFI_CHOICES = [('0', '✘'), ('1', '☕')]
POWER_CHOICES = [('0', '✘'), ('1', '☕')]

class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    cafe_map_url = StringField('Cafe Map URL', validators=[DataRequired()])
    cafe_img_url = StringField('Cafe IMG URL', validators=[DataRequired()])
    cafe_location = StringField('Cafe Location', validators=[DataRequired()])
    cafe_has_sockets = BooleanField('Cafe Socket Availability', false_values={False, 'false', '', None, 'False'})
    cafe_has_toilet = BooleanField('Cafe Toilet Availability', false_values={False, 'false', '', None, 'False'})
    cafe_has_wifi = BooleanField('Cafe WiFi Availability', false_values={False, 'false', '', None, 'False'})
    cafe_can_take_calls = BooleanField('Cafe Call Availability', false_values={False, 'false', '', None, 'False'})
    cafe_seats = IntegerField('Cafe Seat Number', validators=[DataRequired()])
    cafe_coffee_price = FloatField('Cafe Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Cafes(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250) , nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods = ['GET', 'POST'])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():
        new_post = Cafes(
        name=form.cafe_name.data,
        map_url = form.cafe_map_url.data,
        img_url = form.cafe_img_url.data,
        location = form.cafe_location.data,
        has_sockets = form.cafe_has_sockets.data,
        has_toilet = form.cafe_has_toilet.data,
        has_wifi = form.cafe_has_wifi.data,
        can_take_calls = form.cafe_can_take_calls.data,
        seats = form.cafe_seats.data,
        coffee_price = form.cafe_coffee_price.data
        )
        db.session.add(new_post)
        db.session.commit()

        return redirect("/cafes")

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes', methods = ['GET', 'POST'])
def cafes():
    list_of_rows = Cafes.query.all()
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
