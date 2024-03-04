# NOTE: “The FlaskForm base class is defined by the Flask-WTF extension
# so it is imported from flask_wtf. The fields and validators
# however, are imported directly from the WTForms package.”
from flask_wtf import FlaskForm  # Flask WebDev p. 114
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# Information on validators on Flask WebDev p. 212
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from wtforms import ValidationError
from ..models import User


# Flask-WTF web forms is represented in the server by a class
# The class inherits from FlaskForm
class LoginForm(FlaskForm):  # Flask WebDev p. 114 / 132
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()
        ]
    )
    password = PasswordField('Password', validators=[
            DataRequired(), Length(min=11)
        ]
    )
    remember_me = BooleanField('Keep me logged in')  # Booleanfield class represents a checkbox
    # SubmitField class represents a HTML <input type="submit"> in the rendered form
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(11), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
