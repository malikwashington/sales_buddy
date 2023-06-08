from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, TextAreaField
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
  
  

class ContactForm(FlaskForm):
  '''form for creating new contacts'''
  
  f_name = StringField('First Name', validators=[InputRequired(), Length(min=2, max=20)])
  l_name = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=20)])
  phone = StringField('Phone Number', validators=[InputRequired(), Length(min=10, max=20)])
  linkedin = StringField('LinkedIn', validators=[InputRequired(), Length(min=2, max=100)])
  email = StringField('Email', validators=[InputRequired(), Email()])  
  company = StringField('Company', validators=[InputRequired(), Length(min=2, max=100)])
  notes = TextAreaField('Notes', validators=[Length(min=2, max=1000)])
  urgency = SelectField('Urgency', choices=[0,1,2,3,4,5,6,7,8,9,10],default=0)
  potential = SelectField('Potential', choices=[0,1,2,3,4,5,6,7,8,9,10],default=0)
  opportunity = SelectField('Opportunity', choices=[0,1,2,3,4,5,6,7,8,9,10],default=0)
  
class ChangePasswordForm(FlaskForm):
  '''form for changing password'''
  
  old_password = PasswordField('Old Password', validators=[InputRequired()])
  new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=6, max=20)])
  new_password2 = PasswordField('Confirm New Password', validators=[InputRequired(), EqualTo('new_password', message='Passwords must match')])

class SequenceForm(FlaskForm):
  '''form for creating new sequences'''
  
  sequence_name = StringField('Sequence Name', validators=[InputRequired(), Length(min=2, max=20)])
  step_1 = SelectField('Step 1', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_1_notes = TextAreaField('Step 1 Notes')
  step_2 = SelectField('Step 2', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_2_notes = TextAreaField('Step 2 Notes')
  step_3 = SelectField('Step 3', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_3_notes = TextAreaField('Step 3 Notes')
  step_4 = SelectField('Step 4', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_4_notes = TextAreaField('Step 4 Notes')
  step_5 = SelectField('Step 5', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_5_notes = TextAreaField('Step 5 Notes')
  step_6 = SelectField('Step 6', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_6_notes = TextAreaField('Step 6 Notes')
  step_7 = SelectField('Step 7', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_7_notes = TextAreaField('Step 7 Notes')
  step_8 = SelectField('Step 8', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_8_notes = TextAreaField('Step 8 Notes')
  step_9 = SelectField('Step 9', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_9_notes = TextAreaField('Step 9 Notes')
  step_10 = SelectField('Step 10', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_10_notes = TextAreaField('Step 10 Notes')
  step_11 = SelectField('Step 11', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_11_notes = TextAreaField('Step 11 Notes')
  step_12 = SelectField('Step 12', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_12_notes = TextAreaField('Step 12 Notes')
  step_13 = SelectField('Step 13', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_13_notes = TextAreaField('Step 13 Notes')
  step_14 = SelectField('Step 14', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_14_notes = TextAreaField('Step 14 Notes')
  step_15 = SelectField('Step 15', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_15_notes = TextAreaField('Step 15 Notes')
  step_16 = SelectField('Step 16', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_16_notes = TextAreaField('Step 16 Notes')
  step_17 = SelectField('Step 17', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_17_notes = TextAreaField('Step 17 Notes')
  step_18 = SelectField('Step 18', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_18_notes = TextAreaField('Step 18 Notes')
  step_19 = SelectField('Step 19', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_19_notes = TextAreaField('Step 19 Notes')
  step_20 = SelectField('Step 20', choices=[('call', 'Call'), ('email', 'Email'), ('text', 'Text')])
  step_20_notes = TextAreaField('Step 20 Notes')