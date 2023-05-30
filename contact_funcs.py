from datetime import datetime
from model import Contact, Email_Record, Call_Record, Text_Record, db


def add_call_to_contact(contact, from_='Unknown', call_notes=None, call_time=datetime.utcnow()):
    """Add a call to a contact"""

    contact.call_history.append(Call_Record(
        call_time=call_time, from_=from_, call_notes=call_notes))
    db.session.add(contact)
    db.session.commit()

    return contact

def add_sms_to_contact(contact, from_='Unknown', text_body=None, text_time=datetime.utcnow()):
    """Add a text to a contact"""

    contact.text_history.append(Text_Record(
        text_time=text_time, from_=from_, text_body=text_body))
    db.session.add(contact)
    db.session.commit()

    return contact

def get_calls_by_contact(contact_id):
    """Return all calls belonging to a contact"""

    return Call_Record.query.filter_by(contact_id=contact_id).all()


def add_email_to_contact(contact, body, from_='Unknown', time=datetime.utcnow()):
    """Add an email to a contact"""

    contact.email_history.append(Email_Record(
        email_body=body, from_=from_, email_time=time))
    db.session.add(contact)
    db.session.commit()

    return contact


def get_emails_by_contact(contact_id):
    """Return all emails belonging to a contact"""

    return Email_Record.query.filter_by(contact_id=contact_id).all()


def add_text_to_contact(contact, body, from_='Unknown', time=datetime.utcnow()):
    """Add a text to a contact"""

    contact.text_history.append(Text_Record(
        text_body=body, from_=from_, text_time=time))
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
