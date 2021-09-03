from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError

from models.country import Country


class StateForm(FlaskForm):
    name = TextField("Name", [validators.Required("Please enter state name.")])
    country = SelectField("Country", choices=[ (data['id'], data['name']) for data in Country.list()])


class EditStateForm(FlaskForm):
    id = TextField("Id", [validators.Required("Please enter id of state.")])
    name = TextField("Name", [validators.Required("Please enter state name.")])
    country = SelectField("Country", choices=[ (data['id'], data['name']) for data in Country.list()])
    country_id = TextField("Country Id", [validators.Required("Please enter id of country.")])
