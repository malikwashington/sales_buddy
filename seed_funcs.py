from model import Contact, Email_Record, Call_Record, Text_Record, db

def add_call_to_contact(contact, call_time=None):
  """Add a call to a contact and update last_contacted"""

  call_time = datetime.utcnow().strftime('%Y%m%d,%H%M%S') if not call_time else call_time
  contact.last_contacted = call_time
  contact.call_history.append(Call_Record(
      call_time=call_time, to=contact.phone))
  db.session.add(contact)
  db.session.commit()

  return contact
  
  
def add_text_to_contact(contact, body, time=None):
  """Add a text to a contact"""
  
  time = datetime.utcnow().strftime('%Y%m%d,%H%M%S') if not time else time
  contact.text_history.append(Text_Record(
      text_body=body, to=contact.phone, text_time=time))
  db.session.add(contact)
  db.session.commit()

  return contact


def add_email_to_contact(contact, body, time=None):
  """Add an email to a contact"""

  time = datetime.utcnow().strftime('%Y%m%d,%H%M%S') if not time else time
  contact.email_history.append(Email_Record(
      email_body=body, to=contact.email, email_time=time))
  db.session.add(contact)
  db.session.commit()

  return contact

  
if __name__ == '__main__':
  print('seed_funcs.py')
    