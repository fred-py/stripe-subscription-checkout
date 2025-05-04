# NOTE: “The FlaskForm base class is defined by the Flask-WTF extension
# so it is imported from flask_wtf. The fields and validators
# however, are imported directly from the WTForms package.”
from flask_wtf import FlaskForm  # Flask WebDev p. 114
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FormField
# Information on validators on Flask WebDev p. 212
from wtforms.validators import DataRequired, Email, Length, ValidationError
import re



# Flask-WTF web forms is represented in the server by a class
# The class inherits from FlaskForm
# NOTE: this form is not in use
class RegisterInterestForm(FlaskForm):  # Flask WebDev p. 114
    """This class defines a list of fields in the form,
        each field obj can have one of more validators attached."""
    # 1. StringField class represents a HTML <input type="text"> in the rendered form
    # 2. The first argument to the StringField constructor
    #    is the label that will be used when rendering the form
    # 3. The optional validator argument in the StringField constructor
    #    defines a list of checkers applied to the submitted data before it is accepted
    # 4. DataRequired checks that the field is not submitted empty
    # 5. If the field is submitted empty, the validator will prevent
    #    the form from being submitted and prompt the used to complete required fields
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    service = SelectField(
        'Which Plan or Service are you interested in?',
        choices=[
            ('', 'Select...'),
            ('gold', 'Gold Subscription'),
            ('silver', 'Silver Subscription'),
            ('bronze', 'Bronze Subscription'),
            ('one_off_res', 'One-Off residential'),
            ('one_off_comm', 'One-Off Commercial'),
            ('custom_comm', 'Customised Cleaning(Commercial)')
        ],
        validators=[DataRequired(message='Please select a service')]

    )
    # NOTE: Message field not currently in use for residential customers
    message = TextAreaField('Message')
    # SubmitField class represents a HTML <input type="submit"> in the rendered form
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):  # Flask WebDev p. 114
    """This class defines a list of fields in the form,
        each field obj can have one of more validators attached."""
    # 1. StringField class represents a HTML <input type="text"> in the rendered form
    # 2. The first argument to the StringField constructor
    #    is the label that will be used when rendering the form
    # 3. The optional validator argument in the StringField constructor
    #    defines a list of checkers applied to the submitted data before it is accepted
    # 4. DataRequired checks that the field is not submitted empty
    # 5. If the field is submitted empty, the validator will prevent
    #    the form from being submitted and prompt the used to complete required fields
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    service = SelectField(
        'Which Plan or Service are you interested in?',
        choices=[
            ('', 'Select...'),
            ('one_off_res', 'One-Off residential'),
        ],
        validators=[DataRequired(message='Please select a service')]

    )
    # NOTE: Message field not currently in use for residential customers
    message = TextAreaField('Message')
    # SubmitField class represents a HTML <input type="submit"> in the rendered form
    submit = SubmitField('Submit')


class CommercialForm(FlaskForm):  # Flask WebDev p. 114
    """This class defines a list of fields in the form,
        each field obj can have one of more validators attached."""
    # 1. StringField class represents a HTML <input type="text"> in the rendered form
    # 2. The first argument to the StringField constructor
    #    is the label that will be used when rendering the form
    # 3. The optional validator argument in the StringField constructor
    #    defines a list of checkers applied to the submitted data before it is accepted
    # 4. DataRequired checks that the field is not submitted empty
    # 5. If the field is submitted empty, the validator will prevent
    #    the form from being submitted and prompt the used to complete required fields
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired()])
    service = SelectField(
        'Which Plan or Service are you interested in?',
        choices=[
            ('', 'Select...'),
            ('one_off_comm', 'One-Off Commercial'),
            ('custom_comm', 'Customised Cleaning(Commercial)')
        ],
        validators=[DataRequired(message='Please select a service')]

    )
    message = TextAreaField('Message')
    # SubmitField class represents a HTML <input type="submit"> in the rendered form
    submit = SubmitField('Submit')