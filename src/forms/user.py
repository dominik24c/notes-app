from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, Field, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from ..models import User


class BaseUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=128)])


class RegistrationForm(BaseUserForm):
    first_name = StringField('First name', validators=[InputRequired(), Length(min=2, max=64)])
    last_name = StringField('Last name', validators=[InputRequired(), Length(min=2, max=64)])
    email = EmailField('Email', validators=[InputRequired(), Length(max=128)])
    confirm_password = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def _validate_unique(self, error_msg: str, filtered_data: dict) -> None:
        if User.query.filter_by(**filtered_data).first():
            raise ValidationError(error_msg)

    def validate_username(self, field: Field) -> None:
        self._validate_unique("Username already in use!", {"username": field.data})

    def validate_email(self, field: Field) -> None:
        self._validate_unique("Email already in use!", {"email": field.data})


class LoginForm(BaseUserForm):
    submit = SubmitField('Login')
