from twilio.twiml.voice_response import VoiceResponse, Connect, Stream
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
  

def send_call(contact):
  '''make a phone call'''

  call = client.calls.create(
    to=contact,
    from_='+18559126913',
    url='https://handler.twilio.com/twiml/EHe938eb74859553c7722a6c0f731e7fb3'
  )
  
  print(call.sid)
  
  
