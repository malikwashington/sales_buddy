
from twilio.rest import Client
import keys

client = Client(keys.TWILIO_USERNAME, keys.TWILIO_PASSWORD)

def send_text(contact, text):
  '''send a text'''
  message = client.messages.create(
    to=contact,
  from_='+18559126913',
    body=text)
  print(message.sid)