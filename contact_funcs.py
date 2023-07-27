from datetime import datetime
from model import Contact, Email_Record, Call_Record, Text_Record, db

def add_call_to_contact(contactid, name='test user', call_time=None):
  """Add a call to a contact and update last_contacted"""

  contact = get_contact_by_id(contactid)
  call_time = datetime.utcnow().strftime('%Y%m%d,%H%M%S') if not call_time else call_time
  contact.last_contacted = call_time
  contact.call_history.append(Call_Record(
      call_time=call_time, to=contact.phone, caller=name))
  db.session.add(contact)
  db.session.commit()

  return contact

def add_sms_to_contact(contactid, text_body, name='test user'):
  """Add a text to a contact"""

  contact = get_contact_by_id(contactid)
  text_time = datetime.utcnow().strftime('%Y%m%d,%H%M%S')
  contact.last_contacted = text_time
  contact.text_history.append(Text_Record(
      text_time=text_time, to=contact.phone, text_body=text_body, sender=name))
  db.session.add(contact)
  db.session.commit()

  return contact


def add_email_to_contact(contactid, subject, body, name='test user', from_=None, time=None):
  """Add an email to a contact"""

  time = datetime.utcnow().strftime('%Y%m%d,%H%M%S') if not time else time
  contact = get_contact_by_id(contactid)
  
  if not from_:
  #for sent emails
    contact.last_contacted = time
    contact.email_history.append(Email_Record(
      email_subject=subject, email_body=body, to=contact.email, email_time=time, sender=name))
  
  else:
  #for received emails
    contact.last_contacted = time
    contact.email_history.append(Email_Record(
      email_subject=subject, email_body=body, to=name, email_time=time, sender=from_))  
    
  db.session.add(contact)
  db.session.commit()

  return contact



def delete_contact(contact_id):
  '''deletes a contact by id'''
  
  contact = get_contact_by_id(contact_id)
  db.session.delete(contact)
  db.session.commit() 

  return get_contact_by_id(contact_id) == None
  
def get_contact_by_id(contact_id):
  '''gets a contact by id'''  
  
  contact = Contact.query.filter(Contact.contact_id==contact_id).first()
  return contact


def get_calls_by_contact(contact_id):
  """Return all calls belonging to a contact"""

  return Call_Record.query.filter_by(contact_id=contact_id).all()


def get_emails_by_contact(contact_id):
  """Return all emails belonging to a contact"""

  return Email_Record.query.filter_by(contact_id=contact_id).all()


def add_text_to_contact(contact, body, time=None):
  """Add a text to a contact"""
  
  time = datetime.utcnow().strftime('%Y%m%d,%H%M%S') if not time else time
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
  last_contacted = contact.last_contacted or datetime.utcnow()
  p =(contact.urgency+contact.potential+contact.opportunity)/(1+(datetime.utcnow()-last_contacted).days)
  contact.priority = p
  return p

  
def edit_contact(contact_id, f_name, l_name, phone, linkedin, email, company, notes, urgency, potential, opportunity):
  '''edits a contact'''
  contact = get_contact_by_id(contact_id)
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

  
def edit_contact_notes(contact_id, notes):
  '''edits a contact's notes'''
  contact = get_contact_by_id(contact_id)
  contact.notes = notes
  db.session.commit()
  return contact
