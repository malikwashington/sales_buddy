"""Models for  app."""
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
  """A user."""
  
  __tablename__ = "users"
  
  user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String, unique=True, nullable=False)
  password = db.Column(db.String, nullable=False)
  
  contacts = db.relationship('Contact', backref='user')

  def __repr__(self):
    return f'<User user_id={self.user_id} email={self.email}'

class Contact(db.Model):
  '''A contact'''
  
  __tablename__ = "contacts" 
  
  contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
  f_name = db.Column(db.String(25), nullable=False)
  l_name = db.Column(db.String(25), nullable=False)
  linkedin = db.Column(db.String(100), nullable=True)
  email = db.Column(db.String(100), nullable=True)
  company = db.Column(db.String(100), nullable=True)
  notes = db.Column(db.Text, nullable=True)
  urgency = db.Column(db.Integer, nullable=False, default=0)
  potential = db.Column(db.Integer, nullable=False, default=0)
  opportunity = db.Column(db.Integer, nullable=False, default=0)
  date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  last_contacted = db.Column(db.DateTime, nullable=True)
  
  call_history = db.relationship('Call_Record', backref='contact')
  email_history = db.relationship('Email_Record', backref='contact')
  text_history = db.relationship('Text_Record', backref='contact')
  
  user = db.relationship('User', backref='contacts')
  
  def __repr__(self):
    return f'<Contact contact_id={self.contact_id} f_name={self.f_name} l_name={self.l_name}>'

class Call_Record(db.Model):
  '''A call record for a contact'''
  
  __tablename__ = "call_history"
  
  contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id')) 
  call_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  call_notes = db.Column(db.Text, nullable=True)
  
  def __repr__(self):
    return f'<Call_Record call_id={self.call_id} for contact_id={self.contact_id}>'
  
class Email_Record(db.Model):
  '''An email record for a contact'''
  
  __tablename__ = "email_history"
  
  contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'))
  email_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email_body = db.Column(db.Text, nullable=False)
  
  def __repr__(self):
    return f'<Email_Record email_id={self.email_id} for contact_id={self.contact_id}>'

class Text_Record(db.Model):
  '''A text record for a contact'''
  
  __tablename__ = "text_history"
  
  contact_id = db.Column(db.Integer, db.ForeignKey('contacts.contact_id'))
  text_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  text_body = db.Column(db.Text, nullable=False)
  
  def __repr__(self):
    return f'<Text_Record text_id={self.text_id} for contact_id={self.contact_id}>'

def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
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
    
    connect_to_db(app)
    # os.system(f'dropdb {name} --if-exists')
    # os.system(f'createdb {name}')
