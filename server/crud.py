"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def get_users():
    """Return all users."""

    return User.query.all()
  
  
def get_contacts_by_user(user_id):
  """Return all contacts belonging to a user"""
  
  return Contact.query.filter(Contact.user_id == user_id).all()