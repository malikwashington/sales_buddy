from keys import EMAIL, MAIL_PASSWORD, CAL_PASSWORD, ADMIN, ADMIN_KEY
import ssl
import smtplib
from email.message import EmailMessage
from datetime import datetime
from contact_funcs import add_email_to_contact

def send_mail(name, id, to, subject, body, attachment=None):
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

  contact = add_email_to_contact(id, subject, body, name)
  return contact


def admin(subject, to, body):
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
  
  