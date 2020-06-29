from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp

class MovieForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    release_date = StringField(
        'release_date', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    film_summary = StringField(
        'film_summary'
    )

class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    gender = StringField(
        'gender', validators=[DataRequired()]
    )
    age = StringField(
        'age', validators=[DataRequired()]
    )
    contact = StringField(
        'contact'
    )
    place_of_birth = StringField(
        'place_of_birth'
    )
    image_link = StringField(
        'image_link'
    )
    has_bio = BooleanField(
        'has_bio'
    )
    bio = StringField(
        'bio'
    )

