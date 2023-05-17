"""CRUD operations."""

from model import User, Contact
# from server import app

def create_user(email, password):
  """Create and return a new user."""

  user = User(email=email, password=password)

  return user

def get_users():
  """Return all users."""

  return User.query.all()
  
def get_user_by_email(email):
  """Return a user by email."""

  return User.query.filter(User.email.lower() == email.lower()).first()



def add_contact_to_user(user, f_name, l_name, urgency=0, potential=0, opportunity=0,
                        phone=None, linkedin=None, email=None, company=None, notes=None): 
  """Add a contact to a user"""
  
  contact = Contact(user=user, f_name=f_name, l_name=l_name, phone=phone, 
                    linkedin=linkedin, email=email, company=company, notes=notes, 
                    urgency=urgency, potential=potential, opportunity=opportunity)
  print(contact.user_id)
  return contact
  
def get_contacts_by_user(user_id):
  """Return all contacts belonging to a user"""
  
  return Contact.query.filter(Contact.user_id == user_id).all()


# if __name__ == '__main__':
  # connect_to_db(app)