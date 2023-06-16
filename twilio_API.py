from twilio.rest import Client
import keys
from re import sub
from model import db, Call_Record, Text_Record
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.twiml.messaging_response import MessagingResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from flask import jsonify
from datetime import datetime

client = Client(keys.TWILIO_USERNAME, keys.TWILIO_PASSWORD)


def token(id):
  """Generate a Twilio token for a user"""

  token = AccessToken(
                    keys.TWILIO_USERNAME, 
                    keys.TWILIO_API_USERNAME, 
                    keys.TWILIO_API_PASSWORD, 
                    identity='Salesforce User')

  voice_grant = VoiceGrant(
                          outgoing_application_sid=keys.TWIML_APP_SID,
                          incoming_allow=True)
  
  token.add_grant(voice_grant)
  token = token.to_jwt()#.decode('utf-8') not used in twilio docs

  return jsonify(identity=id, token=token)

  
def send_sms(contact, text):
  """Send an SMS to a user's contact"""

  phone_number = '+1' + sub('[\D]','',contact.phone)
  print('\n\n\n\n\n\n', type(phone_number), '\n\n\n\n\n\n')
  message = client.messages.create(
      to= phone_number,
      from_= keys.TWILIO_NUMBER,
      body= text)
  print(message.sid)
  # print(message.date_sent)
  sent_time = datetime.utcnow()
  formatted_time = sent_time.strftime('%a, %d %b %Y %H:%M:%S %Z')
  print('\n\n\n\n\n\n', formatted_time, '\n\n\n\n\n\n')
  contact.text_history.append(Text_Record(
                              text_body=text,
                              text_time=sent_time.strftime('%Y%m%d,%H%M%S'),
                              to=message.to,
                              text_sid=message.sid,))
  contact.last_contacted = formatted_time
  db.session.add(contact)
  db.session.commit()

def voice(phone_number):
  """Make a call to a user's contact"""

  resp = VoiceResponse()
  dial = Dial(
            caller_id='+18559126913',
            # number=phone_number,
            
            # action='/handleDialCallStatus',
            # method='POST',
            # record='record-from-answer-dual',
            # recording_status_callback_event='in-progress completed',
            # recording_status_callback='https://myapp.com/recording-handler',
            # recording_status_callback_method='POST',
  )
  dial.number(phone_number)
  resp.append(dial)
  
  return str(resp)


def bot_call(contact):
  '''make a call to a contact's phone number using programmable voice api
      needs a country code and to be a string'''

  call = client.calls.create(
      url='https://handler.twilio.com/twiml/EHe938eb74859553c7722a6c0f731e7fb3',
      # instead of url, use twiml
      # twiml='<Response><Connect><Stream url='wss:'>SOMETHING GOES HERE</Stream></Connect></Response>',
      to=contact.phone,
      from_='+19177372192')

  print(call.sid)

  contact.call_history.append(Call_Record(
                              call_time=datetime.utcnow().strftime('%Y%m%d,%H%M%S'),
                              to=call.to,
                              call_sid=call.sid,))

  db.session.add(contact.call_history)
  db.session.commit()
