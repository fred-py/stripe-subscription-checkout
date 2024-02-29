# NOTE: “The FlaskForm base class is defined by the Flask-WTF extension
# so it is imported from flask_wtf. The fields and validators
# however, are imported directly from the WTForms package.”
from flask_wtf import FlaskForm  # Flask WebDev p. 114
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# Information on validators on Flask WebDev p. 212
from wtforms.validators import DataRequired, Email, EqualTo, Length


# Flask-WTF web forms is represented in the server by a class
# The class inherits from FlaskForm
class LoginForm(FlaskForm):  # Flask WebDev p. 114 / 132
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()
        ]
    )
    password = PasswordField('Password', validators=[
            DataRequired(), Length(min=12)
        ]
    )
    remember_me = BooleanField('Keep me logged in')  # Booleanfield class represents a checkbox
    # SubmitField class represents a HTML <input type="submit"> in the rendered form
    submit = SubmitField('Login')

""""REGISTRATION FORM STILL NEEDS TO BE ADDED REFER TO REPO"""