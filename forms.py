"""Forms for notes app."""
from flask_wtf import FlaskForm

from wtforms import StringField
from wtforms.validators import InputRequired, Length, Email


class RegisterUserForm(FlaskForm):
    """Form for adding a user"""

    username = StringField(
        "Username", validators=[InputRequired(), Length(max=20)])

    password = StringField(
        "Password", validators=[InputRequired(), Length(min=8, max=50)])

    email = StringField(
        "Email Address", validators=[InputRequired(), Email(), Length(max=50)])

    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(max=30)])

    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(max=30)])