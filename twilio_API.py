from twilio.rest import Client
import keys
client = Client(keys.TWILIO_USERNAME, keys.TWILIO_PASSWORD)

def send_sms(number, text):
  """Send an SMS to a user's contact"""
  
  '''number needs a country code and to be a string'''
  
  message = client.messages.create(
                              to=number,
                              from_='+18559126913',
                              body=text)
  print(message.sid)
  
def sms_otp():
  '''send an SMS with an OTP to a user's phone'''