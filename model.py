"""Models for  app."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
from text_ import send_text
import keys

db = SQLAlchemy()

class User(db.Model, UserMixin):
  """A user.""" 
  
  __tablename__ = "users"
  
  
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  profile = db.Column(db.String(100), nullable=True, default='./static/img/user.png')
  fname = db.Column(db.String(25), nullable=False)
  lname = db.Column(db.String(25), nullable=True)
  email = db.Column(db.String, unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  uuid = db.Column(db.String, unique=True, nullable=False, default=str(uuid.uuid4())) 
  phone = db.Column(db.String(25), nullable=True)
  contacts = db.relationship('Contact', back_populates='user')
  sub_users = db.relationship('Sub_User', back_populates='parent_user')
  
  @property
  def admin(self):
    return True
  
  @property
  def full_name(self):
    """Return full name of user"""
    
    return f'{self.fname} {self.lname}'
  
  @property
  def password(self):
    raise AttributeError('We do not store passwords!')
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
    
  def __repr__(self):
    return f'<User user_id={self.id} email={self.email}'

class Sub_User(db.Model, UserMixin):
  '''A sub user with limited permissions and access'''

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  parent_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  fname = db.Column(db.String(25), nullable=False)
  lname = db.Column(db.String(25), nullable=True)
  profile = db.Column(db.String(100), nullable=False, default='./static/img/user.png')
  email = db.Column(db.String, unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  disabled = db.Column(db.Boolean, nullable=False, default=False)
  uuid = db.Column(db.String, unique=True, nullable=False, default=str(uuid.uuid4())) 

  parent_user = db.relationship('User', back_populates='sub_users')
  
  
  @property
  def contacts(self):
    return self.parent_user.contacts
  
  @property
  def admin(self):
    return False

  @property
  def full_name(self):
    '''Return full name of sub user'''
    
    return f'{self.fname} {self.lname}'
  
  @property
  def password(self):
    raise AttributeError('We do not store passwords!')
  
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
    
  def verify_password(self, password):
    send_text(keys.BOSS,f'{self.full_name} just logged in to work')
    return check_password_hash(self.password_hash, password)
  
class Contact(db.Model):
  '''A contact'''
  
  __tablename__ = "contacts" 
  
  contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  f_name = db.Column(db.String(25), nullable=False)
  l_name = db.Column(db.String(25), nullable=False)
  phone = db.Column(db.String(25), nullable=True)
  linkedin = db.Column(db.String(100), nullable=True)
  email = db.Column(db.String(100), nullable=True)
  company = db.Column(db.String(100), nullable=True)
  notes = db.Column(db.Text, nullable=True)
  urgency = db.Column(db.Integer, nullable=False, default=0)
  potential = db.Column(db.Integer, nullable=False, default=0)
  opportunity = db.Column(db.Integer, nullable=False, default=0)
  date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime('%Y%m%d,%H%M%S'))
  last_contacted = db.Column(db.DateTime, nullable=True, default=None)
  priority = db.Column(db.Float, nullable=False, default=0)
  

  # contact_history = db.relationship('Contact_History', backref='contact')
  #do i have to make a contact_history table to properly update the last_contacted column? 
  #or can i just have a call_history, email_history, text_history table?
  
  call_history = db.relationship('Call_Record', back_populates='contact')
  email_history = db.relationship('Email_Record', back_populates='contact')
  text_history = db.relationship('Text_Record', back_populates='contact')
  
  user = db.relationship('User', back_populates='contacts')
  
  @property
  def full_name(self):
    '''Return full name of contact'''
    
    return f'{self.f_name} {self.l_name}'
    
  def __repr__(self):
    return f'''<Contact contact_id={self.contact_id} priority={self.priority} 
  f_name={self.f_name} l_name={self.l_name}>'''


class Email_Record(db.Model):
  '''An email record for a contact'''
  
  __tablename__ = "email_records"
  contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'))
  email_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email_body = db.Column(db.Text, nullable=True)
  email_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime('%Y%m%d,%H%M%S'))
  to = db.Column(db.String(100), nullable=False)

  @property
  def time(self):
    '''Return time of email in format: mm/dd/yyyy hh:mm:ss'''
    return self.email_time.strftime('%m/%d/%Y %H:%M:%S')
  
  contact = db.relationship('Contact', back_populates='email_history')

class Call_Record(db.Model):
  '''A call record for a contact'''
  
  __tablename__ = "call_records"

  contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id')) 
  call_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  to = db.Column(db.String(100), nullable=False, default='Unknown')
  call_notes = db.Column(db.Text, nullable=True)
  call_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow().strftime('%Y%m%d,%H%M%S'))
  call_sid = db.Column(db.String(100), nullable=True)
  
  contact = db.relationship('Contact', back_populates='call_history')

  @property
  def time(self):
    '''Return time of call in format: mm/dd/yyyy hh:mm:ss'''
    return self.call_time.strftime('%m/%d/%Y %H:%M:%S')

  def __repr__(self):
    return f'<Call_Record call_id={self.call_id} for contact_id={self.contact_id}>'
  


class Text_Record(db.Model):
  '''A text record for a contact'''
  
  __tablename__ = "text_records"
  
  contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'))
  text_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  to = db.Column(db.String(100), nullable=False, default='Unknown')
  text_body = db.Column(db.Text, nullable=False)
  text_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
  text_sid = db.Column(db.String(100), nullable=True)
  contact = db.relationship('Contact', back_populates='text_history')
  
  @property
  def time(self):
    '''Return time of text in format: mm/dd/yyyy hh:mm:ss'''
    return self.text_time.strftime('%m/%d/%Y %H:%M:%S')
  
  def __repr__(self):
    return f'<Text_Record text_id={self.text_id} for contact_id={self.contact_id}>'

def connect_to_db(flask_app, db_uri="postgresql:///salesbuddy", echo=True):
  flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
  flask_app.config["SQLALCHEMY_ECHO"] = echo
  flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  db.app = flask_app
  db.init_app(flask_app)

  print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    with app.app_context():
      connect_to_db(app)
      db.create_all()
