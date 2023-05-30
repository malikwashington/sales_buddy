from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
import email_validator

from model import User
# from flask_login import current_user
# from flask_wtf.file import FileField, FileAllowed
# from wtforms.fields.html5 import DateField



class RegistrationForm(FlaskForm):
  '''Registration form'''
  fname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=20)])
  lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[InputRequired(), Email()])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
  password2 = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
  submit = SubmitField('Submit')

class SignInForm(FlaskForm):
  '''sign in form'''

  email = StringField('Email', validators=[InputRequired(), Email()])
  password = PasswordField('Password', validators=[InputRequired()])
  submit = SubmitField('Sign In')
  
  
class CreateContactForm(FlaskForm):
  '''form for creating new contacts'''

  
class UpdateContactForm(FlaskForm):
  '''form to update existing contacts'''
  
  

class ContactForm(FlaskForm, contact= None):
  '''form for creating new contacts'''
  
  fname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=20)], default=contact.fname or '')
  lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=20)], default=contact.lname or '')
  phone = StringField('Phone Number', validators=[InputRequired(), Length(min=10, max=20)], default=contact.phone or '')
  linkedin = StringField('LinkedIn', validators=[InputRequired(), Length(min=2, max=100)], default=contact.linkedin or '')
  email = StringField('Email', validators=[InputRequired(), Email()], default=contact.email or '')  
  company = StringField('Company', validators=[InputRequired(), Length(min=2, max=100)], default=contact.company or '')
  notes = StringField('Notes', validators=[InputRequired(), Length(min=2, max=1000)], default=contact.notes or '')
  urgency = SelectField('Urgency', choices=[(0, 'Not Urgent'), (1, 'Urgent'), (2, 'Very Urgent')], default=contact.urgency or 0)
  potential = SelectField('Potential', choices=[(0, 'Not Interested'), (1, 'Interested'), (2, 'Very Interested')], default=contact.potential or 0)
  opportunity = SelectField('Opportunity', choices=[(0, 'No Opportunity'), (1, 'Opportunity'), (2, 'Great Opportunity')], default=contact.opportunity or 0)
  submit = SubmitField('Submit')
  
class SequenceForm(FlaskForm):
  '''form for creating new sequences'''
  
  sequence_name = StringField('Sequence Name', validators=[InputRequired(), Length(min=2, max=20)])
  step_1 = SelectField('Step 1', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  