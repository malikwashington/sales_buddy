from twilio.rest import Client
import keys
client = Client(keys.TWILIO_USERNAME, keys.TWILIO_PASSWORD)
# from datetime import datetime

def send_sms(contact, text):
  """Send an SMS to a user's contact"""
  
  prefix = '+1'

  message = client.messages.create(
                              to=prefix + contact.phone,
                              from_='+18559126913',
                              body=text)
  print(message.sid)
  contact.text_history.append(Text_Record(
                              text_body=text, 
                              text_time=message.date_sent,
                              from_=message.from_))
  contact.last_contacted = message.date_sent
  db.sesion.add(contact.text_history)
  db.session.commit()
  

def sms_otp():
  '''send an SMS with an OTP to a user's phone'''


def sms_link():
  '''send an SMS with a link to a user's phone'''
  pass


def sms_reminder():
  '''send an SMS reminder to a user's phone'''
  pass

def call_phone(contact):
  '''make a call to a user's phone number needs a country code and to be a string'''
  
  call = client.calls.create(
                          url='http://demo.twilio.com/docs/voice.xml',
                          to=contact.phone,
                          from_='+18559126913'
                      ) 
  print(call.sid)