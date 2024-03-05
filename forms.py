"""Forms for notes app."""
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class RegisterUserForm(FlaskForm):
    """Form for adding a user"""

    username = StringField(
        "Username", validators=[InputRequired(), Length(max=20)])

    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=50)])

    email = StringField(
        "Email Address", validators=[InputRequired(), Email(), Length(max=50)])

    first_name = StringField(
        "First Name", validators=[InputRequired(), Length(max=30)])

    last_name = StringField(
        "Last Name", validators=[InputRequired(), Length(max=30)])

class LoginUserForm(FlaskForm):
    """Form for logging in"""

    username = StringField(
        "Username", validators=[InputRequired(), Length(max=20)])

    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=50)])


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""