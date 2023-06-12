from datetime import datetime
from model import Contact, Email_Record, Call_Record, Text_Record, db
from user_funcs import get_contact_by_id, delete_contact_by_id

def add_call_to_contact(contact, call_notes=None, call_time=datetime.utcnow()):
  """Add a call to a contact"""

  contact.call_history.append(Call_Record(
      call_time=call_time, to=contact.phone, call_notes=call_notes))
  db.session.add(contact)
  db.session.commit()

  return contact

def add_sms_to_contact(contact, text_body=None, text_time=datetime.utcnow()):
  """Add a text to a contact"""

  contact.text_history.append(Text_Record(
      text_time=text_time, to=contact.phone, text_body=text_body))
  db.session.add(contact)
  db.session.commit()

  return contact

def get_calls_by_contact(contact_id):
  """Return all calls belonging to a contact"""

  return Call_Record.query.filter_by(contact_id=contact_id).all()


def add_email_to_contact(contact, body, time=datetime.utcnow()):
  """Add an email to a contact"""

  contact.email_history.append(Email_Record(
      email_body=body, to=contact.email, email_time=time))
  db.session.add(contact)
  db.session.commit()

  return contact


def get_emails_by_contact(contact_id):
  """Return all emails belonging to a contact"""

  return Email_Record.query.filter_by(contact_id=contact_id).all()


def add_text_to_contact(contact, body, time=datetime.utcnow()):
  """Add a text to a contact"""

  contact.text_history.append(Text_Record(
      text_body=body, to=contact.phone, text_time=time))
  db.session.add(contact)
  db.session.commit()

  return contact


def get_texts_by_contact(contact_id):
  """Return all texts belonging to a contact"""

  return Text_Record.query.filter_by(contact_id=contact_id).all()


def set_priority(contact):
  '''defines the priority of a contact based on the urgency, potential, and opportunity scores'''

  p =(contact.urgency+contact.potential+contact.opportunity)/(1+(datetime.utcnow()-contact.last_contacted).days)
  contact.priority = p
  return p

def delete_contact(user_id, contact_id):
  '''deletes a contact'''
  
  delete_contact_by_id(user_id, contact_id)
  
  return get_contact_by_id(user_id, contact_id) == None

  
def edit_contact(user_id, contact_id, f_name, l_name, phone, linkedin, email, company, notes, urgency, potential, opportunity):
  '''edits a contact'''
  contact = get_contact_by_id(user_id, contact_id)
  contact.f_name = f_name
  contact.l_name = l_name
  contact.phone = phone
  contact.linkedin = linkedin
  contact.email = email
  contact.company = company
  contact.notes = notes
  contact.urgency = urgency
  contact.potential = potential
  contact.opportunity = opportunity
  db.session.commit()
  return contact

  
def edit_contact_notes(user_id, contact_id, notes):
  '''edits a contact's notes'''
  contact = get_contact_by_id(user_id, contact_id)
  contact.notes = notes
  db.session.commit()
  return contact