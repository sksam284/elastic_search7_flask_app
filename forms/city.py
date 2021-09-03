from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

from wtforms import validators, ValidationError

from models.state import State


class CityForm(FlaskForm):
    name = TextField("Name", [validators.Required("Please enter city name.")])
    state = SelectField("State", choices=[(data['id'], data['name']) for data in State.list("")])


class EditCityForm(FlaskForm):
    id = TextField("Id", [validators.Required("Please enter id of city.")])
    name = TextField("Name", [validators.Required("Please enter city name.")])
    state = SelectField("State", choices=[(data['id'], data['name']) for data in State.list("")])
    state_id = TextField("State Id", [validators.Required("Please enter id of state.")])
