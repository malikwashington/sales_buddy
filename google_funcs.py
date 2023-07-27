from keys import EMAIL, MAIL_PASSWORD, CAL_PASSWORD, ADMIN, ADMIN_KEY
import ssl
import smtplib
import imaplib
from email import message_from_bytes as email
from email.message import EmailMessage
from datetime import datetime
from contact_funcs import add_email_to_contact

def get_emails():
  '''get emails from the gmail server'''

  imap = imaplib.IMAP4_SSL("imap.gmail.com")
  imap.login(EMAIL, MAIL_PASSWORD)

  imap.select("Inbox")

  _, msgnums = imap.search(None, "ALL")
  
  for num in msgnums[0].split():
    if num == b'20':
      break
    _, data = imap.fetch(num, "(RFC822)")
    message = email(data[0][1])

    # print('message number: ', num)
    # print(message['From'])
    # print(message['To'])
    # print(message['Date'])
    # print(message['Subject'])
    # print('content: ')
    for part in message.walk():
      if part.get_content_type() == 'text/plain':
        print('\n\n\n',part.get_payload(),'\n\n\n')

  imap.close()

    
  

def send_mail(name, id, to, subject, body, attachment=None):
  '''send an email to a contact'''
  em = EmailMessage()
  em['From'] = EMAIL
  em['To'] = to
  em['Subject'] = subject
  em.set_content(body)  


  context = ssl.create_default_context()

  with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls(context=context)
    server.login(EMAIL, MAIL_PASSWORD)
    server.send_message(em)

  #add email record to contact
  contact = add_email_to_contact(id, subject, body, name)
  return contact


def admin(subject, to, body):
  '''send an email from the server account'''
  em = EmailMessage()
  em['From'] = ADMIN
  em['To'] = to
  em['Subject'] = subject
  em.set_content(body)  


  context = ssl.create_default_context()

  with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls(context=context)
    server.login(ADMIN, ADMIN_KEY)
    server.send_message(em)


def send_calendar_invite(to, subject, body):
  '''create a calendar invite and send it to the contact and the user'''
  
  