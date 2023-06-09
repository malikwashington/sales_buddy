"""CRUD operations."""

from model import User, Contact, Sub_User, db
from datetime import datetime
# from server import app

def create_user(fname, lname, email, password):
  """Create and return a new user."""

  user = User(fname=fname, lname=lname, email=email.lower(), password=password)

  print(f'\n\n user created: {user} \n\n')
  return user
  

def create_sub_user(parent_user, fname, lname, email, password):
  """Create and return a new sub user."""

  sub_user =\
    Sub_User(parent_user=parent_user, fname=fname, lname=lname, email=email.lower(), password=password)

  print(f'\n\n sub user created: {sub_user} \n\n')
  return sub_user
  
def update_profile(user, fname=None, lname=None, email=None, phone=None, profile=None):
  """Update a user's profile"""

  if fname:
    user.fname = fname
  if lname:
    user.lname = lname
  if email:
    user.email = email
  if profile:
    user.profile = profile
  if phone:
    user.phone = phone

  db.session.add(user)
  db.session.commit()

  return user

def get_user_by_email(email):
  """Return a user by email."""

  return User.query.filter(User.email == email.lower().strip()).first()

def get_user_by_uuid(uuid):
  '''return a user by uuid'''
  
  return User.query.filter(User.uuid == uuid).first()

def login_user(email, password):
  '''checks if email and password match a user in the database 
  returns a tuple of boolean and if true, the user object'''
  user = get_user_by_email(email)
  if user:
    verify = user.verify_password(password)
    if verify:
      return (verify, user)
  return (False,)


def add_contact_to_user(user, f_name, l_name, urgency=0, potential=0, opportunity=0,
                        phone=None, email=None, company=None, notes=None,linkedin=None): 
  """Add a contact to a user"""
  
  contact = Contact(user=user, f_name=f_name, l_name=l_name, phone=phone, 
                    linkedin=linkedin, email=email, company=company, notes=notes, 
                    urgency=urgency, potential=potential, opportunity=opportunity)
  print(contact.user_id)
  return contact
  

def get_contacts_by_user(user_id):
  """Return all contacts belonging to a user"""
  
  return Contact.query.filter(Contact.user_id == user_id).all()


def get_contact_by_id(user_id, contact_id):
  """Return a contact by id"""
  
  return Contact.query.filter(Contact.user_id == user_id, Contact.contact_id == contact_id).first()

def delete_contact_by_id(user_id, contact_id):
  """Delete a contact by id"""
  
  contact = get_contact_by_id(user_id, contact_id)
  db.session.delete(contact)
  db.session.commit()

def get_contact_by_phone(user_id, phone):
  """Return a contact by phone number"""
  
  return Contact.query.filter(Contact.user_id == user_id, Contact.phone == phone).first()


# if __name__ == '__main__':
#   connect_to_db(app)