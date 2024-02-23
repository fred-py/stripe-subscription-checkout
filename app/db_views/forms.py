# NOTE: “The FlaskForm base class is defined by the Flask-WTF extension
# so it is imported from flask_wtf. The fields and validators
# however, are imported directly from the WTForms package.”
from flask_wtf import FlaskForm  # Flask WebDev p. 114
from wtforms import StringField, PasswordField, SubmitField
# Information on validators on Flask WebDev p. 212
from wtforms.validators import DataRequired, Email, EqualTo, Length


# Flask-WTF web forms is represented in the server by a class
# The class inherits from FlaskForm
class SignUp(FlaskForm):  # Flask WebDev p. 114
    """This class defines a list of fields in the form
    each field obj can have one of more validators attached."""
    # 1. StringField class represents a HTML <input type="text"> in the rendered form
    # 2. The first argument to the StringField constructor
    #    is the label that will be used when rendering the form
    # 3. The optional validator argument in the StringField constructor
    #    defines a list of checkers applied to the submitted data before it is accepted
    # 4. DataRequired checks that the field is not submitted empty
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=12)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )
    # SubmitField class represents a HTML <input type="submit"> in the rendered form
    submit = SubmitField('Submit')